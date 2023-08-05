'''
TapTypo tests
'''

from io import StringIO
import json
import unittest
from unittest.mock import patch
import singer

from tap_typo.typo import TapTypo
from test_utils.mock_functions import (
    mock_tap_get_dataset_information_empty, mock_requests_get_test_discover_mode,
    mock_requests_get_test_resume_with_state, mock_requests_get_test_get_simple_audit_dataset,
    mock_requests_get_test_get_simple_streaming_dataset, mock_requests_get_test_multi_page_no_limit,
    mock_requests_post_get_token
)
from test_utils.outputs import (
    TEST_DISCOVER_MODE_OUTPUT, TEST_RESUME_WITH_STATE_OUTPUT,
    TEST_GET_SIMPLE_AUDIT_DATASET_OUTPUT, TEST_GET_SIMPLE_STREAMING_DATASET_OUTPUT,
    TEST_MULTI_PAGE_NO_LIMIT_OUTPUT
)
from test_utils.utils import generate_config

# Singer Logger
LOGGER = singer.get_logger()


class TestTapTypo(unittest.TestCase):
    '''
    TapTypo tests
    '''
    maxDiff = None  # Get the full diff when debugging tests

    @patch('tap_typo.typo.requests.post')
    # Mock get_dataset_information because it's called when TapTypo is initialized
    @patch('tap_typo.typo.TapTypo.get_dataset_information', new=mock_tap_get_dataset_information_empty)
    def test_request_token(self, mock_post):
        '''
        Request an access token from Typo
        '''
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {'token': 'test'}

        with self.assertLogs(LOGGER, level='INFO') as log:
            tap = TapTypo(config=generate_config())

        self.assertEqual(len(log.output), 1)

        expected_headers = {
            'Content-Type': 'application/json'
        }

        expected_payload = {
            'apikey': 'typo_key',
            'secret': 'typo_secret'
        }

        token = tap.request_token()

        mock_post.assert_called_with(
            'https://typo.ai/token',
            data=json.dumps(expected_payload),
            headers=expected_headers,
            timeout=20
        )
        self.assertEqual(token, 'test')

    @patch('tap_typo.typo.requests.post', new=mock_requests_post_get_token)
    @patch('tap_typo.typo.requests.get', new=mock_requests_get_test_discover_mode)
    def test_discover_mode(self):
        '''
        tap-typo will fetch the schema from Typo and construct a catalog
        with the stream information.

        Verified on this test:
        - Discover mode output.
        - Conversion of typo-provided field types into JSON schema types.
        - Detection of key properties from typo-provided data.
        '''

        out = None

        with patch('sys.stdout', new=StringIO()) as mock_stdout, self.assertLogs(LOGGER, level='INFO') as log:
            tap = TapTypo(config=generate_config())
            tap.discover()
            out = mock_stdout.getvalue()

        self.assertEqual(len(log.output), 1)

        self.assertEqual(out, TEST_DISCOVER_MODE_OUTPUT)

    @patch('tap_typo.typo.requests.post', new=mock_requests_post_get_token)
    @patch('tap_typo.typo.requests.get', new=mock_requests_get_test_get_simple_audit_dataset)
    def test_get_simple_audit_dataset(self):
        '''
        Fetch a simple dataset with 2 records from Typo
        '''
        out = None
        with patch('sys.stdout', new=StringIO()) as mock_stdout, self.assertLogs(LOGGER, level='INFO') as log:
            tap = TapTypo(config=generate_config())
            tap.sync()
            out = mock_stdout.getvalue()

        self.assertEqual(len(log.output), 4)

        self.assertEqual(out, TEST_GET_SIMPLE_AUDIT_DATASET_OUTPUT)

    @patch('tap_typo.typo.requests.post', new=mock_requests_post_get_token)
    @patch('tap_typo.typo.requests.get', new=mock_requests_get_test_get_simple_streaming_dataset)
    def test_get_simple_streaming_dataset(self):
        '''
        Fetch a simple dataset with 2 records from Typo
        '''
        out = None
        with patch('sys.stdout', new=StringIO()) as mock_stdout, self.assertLogs(LOGGER, level='INFO') as log:
            tap = TapTypo(config=generate_config(audit_id=None))
            tap.sync()
            out = mock_stdout.getvalue()

        self.assertEqual(len(log.output), 4)

        self.assertEqual(out, TEST_GET_SIMPLE_STREAMING_DATASET_OUTPUT)

    @patch('tap_typo.typo.requests.post', new=mock_requests_post_get_token)
    @patch('tap_typo.typo.requests.get', new=mock_requests_get_test_multi_page_no_limit)
    def test_multi_page_no_limit(self):
        '''
        Fetch two pages of a dataset until records end.
        '''
        out = None
        with patch('sys.stdout', new=StringIO()) as mock_stdout, self.assertLogs(LOGGER, level='INFO') as log:
            tap = TapTypo(config=generate_config(records_per_page=2))
            tap.sync()
            out = mock_stdout.getvalue()

        self.assertEqual(len(log.output), 5)

        self.assertEqual(out, TEST_MULTI_PAGE_NO_LIMIT_OUTPUT)

    @patch('tap_typo.typo.requests.post', new=mock_requests_post_get_token)
    @patch('tap_typo.typo.requests.get', new=mock_requests_get_test_resume_with_state)
    def test_resume_with_state(self):
        '''
        Resume sync by providing state input
        '''
        out = None
        with patch('sys.stdout', new=StringIO()) as mock_stdout, self.assertLogs(LOGGER, level='INFO') as log:
            tap = TapTypo(
                config=generate_config(records_per_page=5),
                state={
                    'bookmarks': {
                        'tap-typo-repository-mock_repository-dataset-mock_dataset-audit-123': {
                            '__typo_record_id': 6
                        }
                    }
                })
            tap.sync()
            out = mock_stdout.getvalue()

        self.assertEqual(len(log.output), 4)

        self.assertEqual(out, TEST_RESUME_WITH_STATE_OUTPUT)


if __name__ == '__main__':
    unittest.main()
