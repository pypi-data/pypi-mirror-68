import json
import sys

import requests
import backoff
import singer
from datetime import datetime
from rfc3339 import rfc3339

from tap_typo.logging import log_backoff, log_critical, log_error, log_info


GOOD_STATUS = [200, 201, 202]
OPTION_DISABLED = -1

TYPO_RECORD_ID_PROPERTY = '__typo_record_id'
TYPO_RESULT_PROPERTY = '__typo_result'
BOOKMARK_PROPERTIES = [TYPO_RECORD_ID_PROPERTY]


def get_tap_stream_id(repository, dataset, audit_id):
    '''
    Generates a stream ID from a Dataset name & Audit ID
    '''
    #stream_id = 'tap-typo-repository-{}-dataset-{}'.format(repository, dataset)
    stream_id = f'tap-typo-{repository}-{dataset}'
    if audit_id:
        return f'{stream_id}-audit-{audit_id}'

    return stream_id


# pylint: disable=unused-argument
def backoff_giveup(exception):
    '''
    Called when backoff exhausts max tries
    '''
    log_critical('Unable to make network requests. Please check your internet connection.')
    sys.exit(1)


class TapTypo():
    '''
    Handles fetching streaming or audit dataset data from Typo
    and outputting to stdout following Singer tap standard.
    '''

    def __init__(self, config, state=None, catalog=None):
        self.config = config.copy()
        self.state = state.copy() if state else {}
        self.token = None

        self.base_url = config['cluster_api_endpoint']
        self.api_key = config['api_key']
        self.api_secret = config['api_secret']
        self.repository = config.get('repository')
        self.dataset = config.get('dataset')
        # audit_id is optional
        self.audit_id = config.get('audit_id')
        self.start_record_id = OPTION_DISABLED
        self.records_per_page = config['records_per_page'] if 'records_per_page' in config else 100
        self.record_limit = config['record_limit'] if 'record_limit' in config else OPTION_DISABLED
        self.output_rfc3339_datetime = config.get('output_rfc3339_datetime', False)

        # Stream properties
        self.key_properties = None
        self.schema = None
        self.stream_id = None

        if catalog:
            log_info('Loading catalog from provided file')
            self.catalog = catalog
        else:
            log_info('Discovering catalog')
            self.catalog = self.get_catalog()

    def fetch_audits(self):
        '''
        Requests Typo for the list of available Dataset's
        '''
        
        url = '{}/audits'.format(
            self.base_url)

        # Get request
        response = self.api_get_request(url)

        status = response[0]
        data = response[2]['data']

        # NOTE: Filter datasets that has models.

        def transform_dataset(d):
            d['is_audit'] = True
            return d
        
        data = [transform_dataset(d) for d in data if d['state'] == 'COMPLETED' and d['schema'] is not None]
        
        # Check Status
        if status != 200:
            log_critical(data['message'])
            sys.exit(1)

        return data

    def fetch_datasets(self):
        '''
        Requests Typo for the list of available Dataset's
        '''
        
        url = '{}/datasets'.format(
            self.base_url)

        # Get request
        response = self.api_get_request(url)

        status = response[0]
        data = response[2]

        # NOTE: Filter datasets that has models.

        def transform_dataset(d):
            d['is_audit'] = False
            return d
        
        data = [transform_dataset(d) for d in data if len(d['models']) > 0]
        
        # Check Status
        if status != 200:
            log_critical(data['message'])
            sys.exit(1)

        return data
    
    
    def fetch_dataset_information(self):
        '''
        Requests Typo for an Audit or Streaming Dataset's basic information
        '''
        if self.audit_id:
            url = '{}/repositories/{}/datasets/{}/audits/{}'.format(
                self.base_url, self.repository, self.dataset, self.audit_id)
        else:
            url = '{}/repositories/{}/datasets/{}'.format(
                self.base_url, self.repository, self.dataset)

        # Get request
        response = self.api_get_request(url)

        status = response[0]
        data = response[2]

        # Check Status
        if status != 200:
            log_critical(data['message'])
            sys.exit(1)

        return data

    def get_catalog_entry(self, data):
        
        key_properties, schema, sqltypes, datetime_formats = self.compute_schema(data)

        repository = data['repository']['name']
        audit_id = None
        if data['is_audit']:
            audit_id = data['id']
            dataset = data['dataset']['name']
        else:
            dataset = data['name']

        stream_id = get_tap_stream_id(repository, dataset, audit_id)

        metadata = singer.metadata.get_standard_metadata(
            schema=schema, schema_name=stream_id,
            key_properties=key_properties)

        index = 0
        total_keys = len(metadata)

        while index < total_keys:
            # NOTE: Check if its metadata for stream
            if len(metadata[index]['breadcrumb']) == 0:
                metadata[index]['metadata']['repository'] = repository
                metadata[index]['metadata']['dataset'] = dataset
                metadata[index]['metadata']['audit_id'] = audit_id
                metadata[index]['metadata']['is-view'] = data['is_audit']
                database_name = data['repository']['name']
                metadata[index]['metadata']['database-name'] = database_name
                row_count = data['total_records']
                metadata[index]['metadata']['row-count'] = row_count
                metadata[index]['metadata']['valid-replication-keys'] = [TYPO_RECORD_ID_PROPERTY]
                metadata[index]['metadata']['selected-by-default'] = False # Datasets are not selected by default.
            else:
                metadata[index]['metadata']['selected-by-default'] = True   # Fields are selected by default.
                field_name = metadata[index]['breadcrumb'][1]
                metadata[index]['metadata']['sql-datatype'] = sqltypes[field_name]
                if field_name in datetime_formats:
                    metadata[index]['metadata']['datetime-format'] = datetime_formats[field_name]
            index += 1

        return {
                'stream': stream_id,
                'tap_stream_id': stream_id,
                'schema': schema,
                'metadata': metadata,
                'key_properties': key_properties,
                'bookmark_properties': [TYPO_RECORD_ID_PROPERTY]
            }

    def compute_schema(self, data):
        typo_schema = data.get('schema')

        schema_properties = {}
        key_properties = [TYPO_RECORD_ID_PROPERTY]

        available_sql_types = {
            'number': 'float',
            'integer': 'int',
            'string': 'varchar(255)',
            'date-time': 'datetime',
            'boolean': 'bool'
        }
        
        DEFAULT_SQL_TYPE = 'varchar(255)'

        sql_types = {}
        datetime_formats = {}

        if typo_schema is not None:
            for field, spec in typo_schema.items():
                if 'primary' in spec and spec['primary']:
                    key_properties.append(field)

                field_type = ''
                field_format = None
                if 'type' in spec:
                    # Only add spec for fields we can identify with certainty
                    if spec['type'] == 'float' or spec['type'] == 'number':
                        field_type = 'number'
                    elif spec['type'] == 'integer' or spec['type'] == 'int' or spec['type'] == 'smallint':
                        field_type = 'integer'
                    elif spec['type'] == 'varchar' or spec['type'] == 'string':
                        field_type = 'string'
                    elif spec['type'] == 'date-time':
                        field_type = 'string'
                        if spec.get('format') is not None and self.output_rfc3339_datetime:
                            field_format = 'date-time'
                            datetime_formats[field] = spec.get('format')
                    else:
                        field_type = 'string'
                    
                    if field_format:
                        schema_properties[field] = {
                            'type': ['null', field_type],
                            'format': field_format }
                    else:
                        schema_properties[field] = {
                            'type': ['null', field_type]
                        }
                    sql_types[field] = available_sql_types.get(field_type, DEFAULT_SQL_TYPE)
                else:
                    schema_properties[field] = {}

        # NOTE: Add Typo specific properties
        schema_properties[TYPO_RESULT_PROPERTY] = {
            'type': 'string'
        }
        sql_types[TYPO_RESULT_PROPERTY] = 'varchar(255)'

        schema_properties[TYPO_RECORD_ID_PROPERTY] = {
            'type': 'integer'
        }
        sql_types[TYPO_RECORD_ID_PROPERTY] = 'int'

        schema = {
            'type': 'object',
            'additionalProperties': True,
            'properties': schema_properties
        }

        return key_properties, schema, sql_types, datetime_formats

    def get_catalog_entries(self):
        '''
        Requests Typo for an Audit or Streaming Dataset's basic information
        and builds the catalog entries metadata.
        '''
        datasets = self.fetch_datasets()
        audits = self.fetch_audits()

        data = datasets + audits

        # Transform dataset information into catalog metadata

        entries = [self.get_catalog_entry(d) for d in data]
        return entries

    def get_catalog(self):
        '''
        Builds the catalog from the provided config
        '''
        catalog_entries = self.get_catalog_entries()
        return {
            'streams': catalog_entries
        }

    def discover(self):
        '''
        Gets the catalog and outputs to stdout
        '''
        catalog = self.get_catalog()
        print(json.dumps(catalog, indent=2))

    # pylint: disable=no-self-use
    @backoff.on_exception(
        backoff.expo,
        (requests.exceptions.Timeout, requests.exceptions.ConnectionError),
        max_tries=8,
        on_backoff=log_backoff,
        on_giveup=backoff_giveup,
        logger=None,
        factor=3
    )
    def post_request(self, url, headers, payload):
        '''
        Generic POST request
        '''
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=20)

        status = response.status_code
        data = response.json()

        # Check response status
        if status not in GOOD_STATUS:
            if isinstance(data, dict) and 'message' in data.keys():
                log_error(('Post request failed. Please verify your config and try again later. Error message: {}. ' +
                           'Request url=[{}], request status_code=[{}].').format(
                               data['message'], url, response.status_code))
            else:
                log_error(('Post request failed. Please verify your config and try again later. url=[{}], ' +
                           'request.status_code=[{}], response.text=[{}].').format(
                               url, response.status_code, response.text))

        return status, data

    @backoff.on_exception(
        backoff.expo,
        (requests.exceptions.Timeout, requests.exceptions.ConnectionError),
        max_tries=8,
        on_backoff=log_backoff,
        on_giveup=backoff_giveup,
        logger=None,
        factor=3
    )
    def get_request(self, url, headers, params=None):
        '''
        Generic GET request
        '''
        response = requests.get(url, headers=headers, params=params, timeout=20)
        status = response.status_code
        data = response.json()
        headers = response.headers

        # Check response status
        if status not in GOOD_STATUS:
            if isinstance(data, dict) and 'message' in data.keys():
                log_error(('Get request failed. Please verify your config and try again later. Error message: {}. ' +
                           'Request url=[{}], request status_code=[{}].').format(
                               data['message'], url, response.status_code))
            else:
                log_error(('Get request failed. Please verify your config and try again later. url=[{}], ' +
                           'request.status_code=[{}], response.text=[{}].').format(
                               url, response.status_code, response.text))
            sys.exit(1)

        return status, headers, data

    def api_get_request(self, url, params=None):
        '''
        Make a GET request to the Typo API
        '''
        if not self.token:
            self.token = self.request_token()

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.token)
        }

        status, response_headers, data = self.get_request(url, headers, params)

        # Expired token
        if status == 401:
            self.token = self.request_token()

            # Retry post_request with new token
            status, response_headers, data = self.get_request(url, headers, params)

        return status, response_headers, data

    def request_token(self):
        '''
        Token Request for other requests
        '''

        # Required parameters
        url = self.base_url.rstrip('/') + '/token'
        headers = {
            'Content-Type': 'application/json'
        }
        payload = {
            'apikey': self.api_key,
            'secret': self.api_secret
        }

        # POST request
        status, data = self.post_request(url, headers, payload)

        # Check Status
        if status != 200:
            log_error(
                'Authorization Token Request Failed. ' +
                'Please check your credentials. Details: ' +
                '{}'.format(data)
            )
            sys.exit(1)

        return data['token']

    def get_page(self, repository, dataset, audit_id, page_number):
        '''
        Fetches one page of results from the Typo API
        '''
        log_info('Fetching page {}.'.format(page_number))

        if audit_id is not None:
            base_url = '{}/repositories/{}/datasets/{}/audits/{}/results'.format(
                self.base_url, repository, dataset, audit_id)
        else:
            base_url = '{}/repositories/{}/datasets/{}/results'.format(
                self.base_url, repository, dataset)

        # Get request
        start_record_id_filter = ''

        if self.start_record_id != OPTION_DISABLED:
            start_record_id_filter = '&__typo_id=gt:{}'.format(self.start_record_id)

        status, headers, data = self.api_get_request('{}?per_page={}&page={}{}'.format(
            base_url, self.records_per_page, page_number, start_record_id_filter))

        # Check Status
        if status != 200:
            log_error(data['message'])
            sys.exit(1)

        eof = not ('Link' in headers and '; rel="next"' in headers['Link'])
        return data, eof

    def get_selected_streams(self):
        '''
        Checks stream schema's metadata looking for an empty breadcrumb that has in it's metadata
        property `selected` set to True or has `selected-by-default` set to True.
        '''
        selected_streams = []

        for stream in self.catalog['streams']:
            stream_metadata = singer.metadata.to_map(stream['metadata'])

            # stream metadata will have an empty breadcrumb
            selected = singer.metadata.get(stream_metadata, (), 'selected')

            if selected or (selected is not False and singer.metadata.get(stream_metadata, (), 'selected-by-default')):
                selected_streams.append(stream['tap_stream_id'])

        return selected_streams

    def setup_tap_from_state(self):
        '''
        Looks into the state for a bookmark corresponding to the current stream, if found,
        it sets up the tap to start from the bookmark.
        '''
        try:
            # Check if there's a bookmark available in the state
            self.start_record_id = self.state['bookmarks'][self.stream_id][TYPO_RECORD_ID_PROPERTY]

            record_limit_log_message = ''

            if self.record_limit and self.record_limit != OPTION_DISABLED:
                record_limit_log_message = ' / Remaining Record Limit: `{}`'.format(self.record_limit)

            log_info((
                'Syncing stream `{}`. Resuming from provided state file. Start Typo record id: {}. ' +
                'Records per page: {}{}.').format(
                    self.stream_id,
                    self.start_record_id,
                    self.records_per_page,
                    record_limit_log_message
                ))

        except KeyError:
            log_info('Syncing stream `{}`. Records per page: {}.{}'.format(
                self.stream_id, self.records_per_page,
                ' Record limit: {}.'.format(self.record_limit) if self.record_limit != OPTION_DISABLED else ''))


    def sync_stream(self, stream):
        self.key_properties = stream['key_properties']
        self.schema = stream['schema']
        self.stream_id = stream['tap_stream_id']
        self.start_record_id = OPTION_DISABLED

        stream_metadata = singer.metadata.to_map(stream['metadata'])
        repository = singer.metadata.get(stream_metadata, (), 'repository')
        dataset = singer.metadata.get(stream_metadata, (), 'dataset')
        audit_id = singer.metadata.get(stream_metadata, (), 'audit_id')

        self.setup_tap_from_state()

        # Output state and schema
        singer.write_state(self.state)
        singer.write_schema(self.stream_id, self.schema, self.key_properties,
                            bookmark_properties=BOOKMARK_PROPERTIES)

        eof = False
        record_count = 0
        record_limit_reached = False
        page_number = 1

        # Get the fields that will need rfc3339 transformations.
        rfc3339_fields_format = {}
        if self.output_rfc3339_datetime:
            for field_path, field_metadata in stream_metadata.items():
                if field_path and 'datetime-format' in field_metadata:  # NOTE: Checking for tuples that are not empty that represent field metadata
                    field_name = field_path[1]
                    rfc3339_fields_format[field_name] = field_metadata['datetime-format']

        while not eof and not record_limit_reached:
            data, eof = self.get_page(repository, dataset, audit_id, page_number)

            for record in data['data']['records']:
                record_count += 1

                # Inserting output results from Typo
                record_data = record['record']

                if record['has_errors']:
                    record_data['__typo_result'] = 'Error'
                else:
                    record_data['__typo_result'] = 'OK'

                record_data[TYPO_RECORD_ID_PROPERTY] = record['id']

                if self.output_rfc3339_datetime:
                    # Iterate fields that needs transformation into rfc3339
                    for field_name, field_format in rfc3339_fields_format.items():
                        original_value = record_data[field_name]
                        parsed_datetime = datetime.strptime(original_value, field_format)
                        rfc3339_datetime = rfc3339(parsed_datetime)
                        record_data[field_name] = rfc3339_datetime

                # Output record
                singer.write_record(self.stream_id, record_data)

                bookmark = record['id']

                self.state = singer.write_bookmark(self.state, self.stream_id, TYPO_RECORD_ID_PROPERTY, bookmark)
                singer.write_state(self.state)

                if (self.record_limit != OPTION_DISABLED
                        and record_count == self.record_limit):
                    record_limit_reached = True
                    log_info('Record limit reached. Finishing syncing for stream `{}`.'.format(self.stream_id))
                    break

            page_number += 1

        if eof:
            log_info('Finished syncing all available data for stream `{}`.'.format(self.stream_id))

    def sync(self, catalog_mode=False):
        '''
        Parse every stream in the catalog, fetch data from Typo and send to stdout
        '''
        
        if catalog_mode:
            selected_streams = self.get_selected_streams()
            for stream in self.catalog['streams']:
                if stream['tap_stream_id'] not in selected_streams:
                    log_info('Skipped stream `{}`: stream not selected for syncing.'.format(stream['tap_stream_id']))
                    continue
                self.sync_stream(stream)
        else:
            if not self.repository and not self.dataset:
                 log_info('Nothing to do as not running in catalog mode and repository, dataset and/or audit_id weren\'t specified in the config file.')
            else:
                repository = self.repository
                dataset = self.dataset
                audit_id = self.audit_id
                stream_id = get_tap_stream_id(repository, dataset, audit_id)
                streams = [stream for stream in self.catalog['streams'] if stream['tap_stream_id'] == stream_id]
                if len(streams) == 0:
                    log_info('Nothing do to. Cannot find a stream for the provided repository, dataset and audit_id config parameters.')
                    return
                self.sync_stream(streams[0])
            
