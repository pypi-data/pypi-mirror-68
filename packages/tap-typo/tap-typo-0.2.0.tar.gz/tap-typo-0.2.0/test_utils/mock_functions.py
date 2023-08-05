'''
Mock functions for testing
'''

from test_utils.utils import generate_record


class MockRequestResponse:  # pylint: disable=too-few-public-methods
    '''
    Mocks requests get/post response
    '''
    def __init__(self, json_data, status_code, headers=None):
        self.json_data = json_data
        self.headers = headers if headers else {}
        self.text = ''
        self.status_code = status_code

    def json(self):
        '''
        Mocks response.json()
        '''
        return self.json_data


def generate_streaming_dataset_header_response():
    '''
    Streaming dataset sample header response
    '''
    return {
        'code': 'GET_DATASET_SUCCESS',
        'message': 'Get dataset success',
        'data': {
            'id': 1,
            'dataset': {
                'schema': {}
            },
            'metadata': None
        }
    }


def generate_audit_dataset_header_response():
    '''
    Audit dataset sample header response
    '''
    return {
        'code': 'GET_AUDIT_SUCCESS',
        'message': 'Get audit success',
        'data': {
            'id': 1,
            'dataset': {
                'schema': {}
            },
            'metadata': None
        }
    }


def generate_audit_dataset_header_response_detailed_schema():
    '''
    Audit dataset sample header response with a detailed schema
    '''
    return {
        'code': 'GET_AUDIT_SUCCESS',
        'message': 'Get audit success',
        'data': {
            'id': 1,
            'dataset': {
                'schema': {
                    'val1': {
                        'primary': True,
                        'type': 'string'
                    },
                    'val2': {
                        'primary': False,
                        'type': 'varchar'
                    },
                    'val3': {
                        'type': 'int'
                    },
                    'val4': {
                        'type': 'integer'
                    },
                    'val5': {
                        'type': 'smallint'
                    },
                    'val6': {
                        'type': 'float'
                    },
                    'val7': {
                        'type': 'unknown'
                    },
                    'val8': {},
                    'val9': {
                        'primary': True
                    },
                }
            },
            'metadata': None
        }
    }


def generate_streaming_dataset_response(records):
    '''
    Simple streaming dataset response
    '''
    return {
        'code': 'GET_DATASET_RESULTS_SUCCESS',
        'message': 'Get Dataset results success',
        'data': {
            'page': 1, 'per_page': 1, 'total_pages': 2,
            'total_records': 5, 'filters': [], 'sort': {},
            'records': records
        }
    }


def generate_audit_dataset_response(records):
    '''
    Simple audit dataset response
    '''
    return {
        'code': 'GET_AUDIT_RESULTS_SUCCESS',
        'message': 'Get Dataset results success',
        'data': {
            'page': 1, 'per_page': 1, 'total_pages': 2,
            'total_records': 5, 'filters': [], 'sort': {},
            'records': records
        }
    }


def mock_tap_get_dataset_information_empty(self):  # pylint: disable=unused-argument
    '''
    Mock get_dataset_information
    '''
    return [], {}


def mock_requests_post_get_token(url, headers, data, timeout):  # pylint: disable=unused-argument
    '''
    Mock get_token
    '''
    return MockRequestResponse({'token': 'test'}, 200)


def mock_requests_get_test_discover_mode(url, headers, params, timeout):  # pylint: disable=unused-argument
    '''
    Mock get requests for test_discover_mode
    '''
    # Return audit header
    if url == 'https://typo.ai/repositories/mock_repository/datasets/mock_dataset/audits/123':
        return MockRequestResponse(generate_audit_dataset_header_response_detailed_schema(), 200)

    raise Exception('This code should not be reached')


def mock_requests_get_test_resume_with_state(url, headers, params, timeout):  # pylint: disable=unused-argument
    '''
    Mock get requests for test_resume_with_state
    '''
    # Return audit header
    if url == 'https://typo.ai/repositories/mock_repository/datasets/mock_dataset/audits/123':
        return MockRequestResponse(generate_audit_dataset_header_response(), 200)

    if url == 'https://typo.ai/repositories/mock_repository/datasets/mock_dataset/audits/123/results?per_page=5&page=1&__typo_id=gt:6':
        # tap-typo will resume from record with id 22
        return MockRequestResponse(generate_audit_dataset_response(
            [generate_record(7, has_errors=True), generate_record(8), generate_record(9),
             generate_record(10), generate_record(11, has_errors=True)]
        ), 200, headers={'Link': ''})

    raise Exception('This code should not be reached')


# pylint: disable=unused-argument
def mock_requests_get_test_get_simple_streaming_dataset(url, headers, params, timeout):
    '''
    Mock get requests for test_get_simple_streaming_dataset
    '''
    # Return audit header
    if url == 'https://typo.ai/repositories/mock_repository/datasets/mock_dataset':
        return MockRequestResponse(generate_streaming_dataset_header_response(), 200)

    if url == 'https://typo.ai/repositories/mock_repository/datasets/mock_dataset/results?per_page=100&page=1':
        # Return 1st and only results page
        return MockRequestResponse(
            generate_streaming_dataset_response(
                [generate_record(1, has_errors=True), generate_record(2)]
            ),
            200, headers={'Link': ''})

    raise Exception('This code should not be reached')


def mock_requests_get_test_get_simple_audit_dataset(url, headers, params, timeout):
    '''
    Mock get requests for test_get_simple_audit_dataset
    '''
    # Return audit header
    if url == 'https://typo.ai/repositories/mock_repository/datasets/mock_dataset/audits/123':
        return MockRequestResponse(generate_audit_dataset_header_response(), 200)

    if (url == 'https://typo.ai/repositories/mock_repository/datasets/mock_dataset/audits/123/results' +
            '?per_page=100&page=1'):
        # Return 1st and only results page
        return MockRequestResponse(
            generate_audit_dataset_response(
                [generate_record(1, has_errors=True), generate_record(2)]
            ),
            200, headers={'Link': ''})

    raise Exception('This code should not be reached')


def mock_requests_get_test_multi_page_no_limit(url, headers, params, timeout):
    '''
    Mock get requests for test_multi_page_no_limit
    '''
    # Return audit header
    if url == 'https://typo.ai/repositories/mock_repository/datasets/mock_dataset/audits/123':
        return MockRequestResponse(generate_audit_dataset_header_response(), 200)

    # Return 1st page of results
    if url == 'https://typo.ai/repositories/mock_repository/datasets/mock_dataset/audits/123/results?per_page=2&page=1':
        return MockRequestResponse(
            generate_audit_dataset_response(
                [generate_record(1, has_errors=True), generate_record(2)]
            ),
            200, headers={'Link': 'mocklink'})

    # Return 2nd page of results
    if url == 'https://typo.ai/repositories/mock_repository/datasets/mock_dataset/audits/123/results?per_page=2&page=2':
        return MockRequestResponse(
            generate_audit_dataset_response(
                [generate_record(3, has_errors=True), generate_record(4)]
            ),
            200, headers={'Link': ''})

    raise Exception('This code should not be reached')
