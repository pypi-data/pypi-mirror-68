'''
Test utility functions
'''

def generate_config(**kwargs):
    '''
    Generates a config file for testing
    '''
    config = {
        'cluster_api_endpoint': 'https://typo.ai',
        'api_key': 'typo_key',
        'api_secret': 'typo_secret',
        'repository': 'mock_repository',
        'dataset': 'mock_dataset',
        'audit_id': '123',
        'state': {},
        'records_per_page': 100,
        'record_limit': -1
    }

    config.update(kwargs)

    return config


def generate_record(record_id, **kwargs):
    '''
    Generates a record API response
    '''
    record = {
        'tag': '',
        'quality_label': 'Not Set',
        'quality_feedback': {
            'date': 'Not Set',
            'typo': 'Good'
        },
        'record': {
            'date': 'today',
            'typo': 'tap'
        },
        'total_models': 3,
        'processed_models': 3,
        'record_hash': 'hash',
        'created_at': '2020-01-27T00:20:35.782Z',
        'tenant_id': 1,
        'repository_id': 1,
        'id': record_id,
        'audit_id': 1,
        'has_errors': False,
        'errors_fields': []
    }

    record.update(kwargs)

    return record
