'''
Test stdout output strings for comparison
'''

TEST_DISCOVER_MODE_OUTPUT = '''{
  "streams": [
    {
      "stream": "tap-typo-repository-mock_repository-dataset-mock_dataset-audit-123",
      "tap_stream_id": "tap-typo-repository-mock_repository-dataset-mock_dataset-audit-123",
      "schema": {
        "type": "object",
        "additionalProperties": true,
        "properties": {
          "val1": {
            "type": [
              "null",
              "string"
            ]
          },
          "val2": {
            "type": [
              "null",
              "string"
            ]
          },
          "val3": {
            "type": [
              "null",
              "integer"
            ]
          },
          "val4": {
            "type": [
              "null",
              "integer"
            ]
          },
          "val5": {
            "type": [
              "null",
              "integer"
            ]
          },
          "val6": {
            "type": [
              "null",
              "number"
            ]
          },
          "val7": {},
          "val8": {},
          "val9": {},
          "__typo_result": {
            "type": "string"
          },
          "__typo_record_id": {
            "type": "integer"
          }
        }
      },
      "metadata": [
        {
          "breadcrumb": [],
          "metadata": {
            "table-key-properties": [
              "__typo_record_id",
              "val1",
              "val9"
            ],
            "inclusion": "available",
            "schema-name": "tap-typo-repository-mock_repository-dataset-mock_dataset-audit-123",
            "selected-by-default": true,
            "valid-replication-keys": [
              "__typo_record_id"
            ]
          }
        },
        {
          "breadcrumb": [
            "properties",
            "val1"
          ],
          "metadata": {
            "inclusion": "automatic",
            "selected-by-default": true
          }
        },
        {
          "breadcrumb": [
            "properties",
            "val2"
          ],
          "metadata": {
            "inclusion": "available",
            "selected-by-default": true
          }
        },
        {
          "breadcrumb": [
            "properties",
            "val3"
          ],
          "metadata": {
            "inclusion": "available",
            "selected-by-default": true
          }
        },
        {
          "breadcrumb": [
            "properties",
            "val4"
          ],
          "metadata": {
            "inclusion": "available",
            "selected-by-default": true
          }
        },
        {
          "breadcrumb": [
            "properties",
            "val5"
          ],
          "metadata": {
            "inclusion": "available",
            "selected-by-default": true
          }
        },
        {
          "breadcrumb": [
            "properties",
            "val6"
          ],
          "metadata": {
            "inclusion": "available",
            "selected-by-default": true
          }
        },
        {
          "breadcrumb": [
            "properties",
            "val7"
          ],
          "metadata": {
            "inclusion": "available",
            "selected-by-default": true
          }
        },
        {
          "breadcrumb": [
            "properties",
            "val8"
          ],
          "metadata": {
            "inclusion": "available",
            "selected-by-default": true
          }
        },
        {
          "breadcrumb": [
            "properties",
            "val9"
          ],
          "metadata": {
            "inclusion": "automatic",
            "selected-by-default": true
          }
        },
        {
          "breadcrumb": [
            "properties",
            "__typo_result"
          ],
          "metadata": {
            "inclusion": "available",
            "selected-by-default": true
          }
        },
        {
          "breadcrumb": [
            "properties",
            "__typo_record_id"
          ],
          "metadata": {
            "inclusion": "automatic",
            "selected-by-default": true
          }
        }
      ],
      "key_properties": [
        "__typo_record_id",
        "val1",
        "val9"
      ],
      "bookmark_properties": [
        "__typo_record_id"
      ]
    }
  ]
}
'''

TEST_RESUME_WITH_STATE_OUTPUT = (
    '{"type": "STATE", "value": {"bookmarks": {"tap-typo-repository-mock_repository-dataset-mock_dataset-audit-123": {"__typo_record_id": 6}}}}\n' + # noqa pylint: disable=line-too-long
    '{"type": "SCHEMA", "stream": "tap-typo-repository-mock_repository-dataset-mock_dataset-audit-123", "schema": {"type": "object", "additionalProperties": true, "properties": {"__typo_result": {"type": "string"}, "__typo_record_id": {"type": "integer"}}}, "key_properties": ["__typo_record_id"], "bookmark_properties": ["__typo_record_id"]}\n' + # noqa pylint: disable=line-too-long
    '{"type": "RECORD", "stream": "tap-typo-repository-mock_repository-dataset-mock_dataset-audit-123", "record": {"date": "today", "typo": "tap", "__typo_result": "Error", "__typo_record_id": 7}}\n' + # noqa pylint: disable=line-too-long
    '{"type": "STATE", "value": {"bookmarks": {"tap-typo-repository-mock_repository-dataset-mock_dataset-audit-123": {"__typo_record_id": 7}}}}\n' + # noqa pylint: disable=line-too-long
    '{"type": "RECORD", "stream": "tap-typo-repository-mock_repository-dataset-mock_dataset-audit-123", "record": {"date": "today", "typo": "tap", "__typo_result": "OK", "__typo_record_id": 8}}\n' + # noqa pylint: disable=line-too-long
    '{"type": "STATE", "value": {"bookmarks": {"tap-typo-repository-mock_repository-dataset-mock_dataset-audit-123": {"__typo_record_id": 8}}}}\n' + # noqa pylint: disable=line-too-long
    '{"type": "RECORD", "stream": "tap-typo-repository-mock_repository-dataset-mock_dataset-audit-123", "record": {"date": "today", "typo": "tap", "__typo_result": "OK", "__typo_record_id": 9}}\n' + # noqa pylint: disable=line-too-long
    '{"type": "STATE", "value": {"bookmarks": {"tap-typo-repository-mock_repository-dataset-mock_dataset-audit-123": {"__typo_record_id": 9}}}}\n' + # noqa pylint: disable=line-too-long
    '{"type": "RECORD", "stream": "tap-typo-repository-mock_repository-dataset-mock_dataset-audit-123", "record": {"date": "today", "typo": "tap", "__typo_result": "OK", "__typo_record_id": 10}}\n' + # noqa pylint: disable=line-too-long
    '{"type": "STATE", "value": {"bookmarks": {"tap-typo-repository-mock_repository-dataset-mock_dataset-audit-123": {"__typo_record_id": 10}}}}\n' + # noqa pylint: disable=line-too-long
    '{"type": "RECORD", "stream": "tap-typo-repository-mock_repository-dataset-mock_dataset-audit-123", "record": {"date": "today", "typo": "tap", "__typo_result": "Error", "__typo_record_id": 11}}\n' + # noqa pylint: disable=line-too-long
    '{"type": "STATE", "value": {"bookmarks": {"tap-typo-repository-mock_repository-dataset-mock_dataset-audit-123": {"__typo_record_id": 11}}}}\n' # noqa pylint: disable=line-too-long
)

TEST_GET_SIMPLE_AUDIT_DATASET_OUTPUT = (
    '{"type": "STATE", "value": {}}\n' +
    '{"type": "SCHEMA", "stream": "tap-typo-repository-mock_repository-dataset-mock_dataset-audit-123", "schema": {"type": "object", "additionalProperties": true, "properties": {"__typo_result": {"type": "string"}, "__typo_record_id": {"type": "integer"}}}, "key_properties": ["__typo_record_id"], "bookmark_properties": ["__typo_record_id"]}\n' + # noqa pylint: disable=line-too-long
    '{"type": "RECORD", "stream": "tap-typo-repository-mock_repository-dataset-mock_dataset-audit-123", "record": {"date": "today", "typo": "tap", "__typo_result": "Error", "__typo_record_id": 1}}\n' + # noqa pylint: disable=line-too-long
    '{"type": "STATE", "value": {"bookmarks": {"tap-typo-repository-mock_repository-dataset-mock_dataset-audit-123": {"__typo_record_id": 1}}}}\n' + # noqa pylint: disable=line-too-long
    '{"type": "RECORD", "stream": "tap-typo-repository-mock_repository-dataset-mock_dataset-audit-123", "record": {"date": "today", "typo": "tap", "__typo_result": "OK", "__typo_record_id": 2}}\n' + # noqa pylint: disable=line-too-long
    '{"type": "STATE", "value": {"bookmarks": {"tap-typo-repository-mock_repository-dataset-mock_dataset-audit-123": {"__typo_record_id": 2}}}}\n' # noqa pylint: disable=line-too-long
)

TEST_GET_SIMPLE_STREAMING_DATASET_OUTPUT = (
    '{"type": "STATE", "value": {}}\n' +
    '{"type": "SCHEMA", "stream": "tap-typo-repository-mock_repository-dataset-mock_dataset", "schema": {"type": "object", "additionalProperties": true, "properties": {"__typo_result": {"type": "string"}, "__typo_record_id": {"type": "integer"}}}, "key_properties": ["__typo_record_id"], "bookmark_properties": ["__typo_record_id"]}\n' + # noqa pylint: disable=line-too-long
    '{"type": "RECORD", "stream": "tap-typo-repository-mock_repository-dataset-mock_dataset", "record": {"date": "today", "typo": "tap", "__typo_result": "Error", "__typo_record_id": 1}}\n' + # noqa pylint: disable=line-too-long
    '{"type": "STATE", "value": {"bookmarks": {"tap-typo-repository-mock_repository-dataset-mock_dataset": {"__typo_record_id": 1}}}}\n' + # noqa pylint: disable=line-too-long
    '{"type": "RECORD", "stream": "tap-typo-repository-mock_repository-dataset-mock_dataset", "record": {"date": "today", "typo": "tap", "__typo_result": "OK", "__typo_record_id": 2}}\n' + # noqa pylint: disable=line-too-long
    '{"type": "STATE", "value": {"bookmarks": {"tap-typo-repository-mock_repository-dataset-mock_dataset": {"__typo_record_id": 2}}}}\n' # noqa pylint: disable=line-too-long
)

TEST_MULTI_PAGE_NO_LIMIT_OUTPUT = (
    '{"type": "STATE", "value": {}}\n' +
    '{"type": "SCHEMA", "stream": "tap-typo-repository-mock_repository-dataset-mock_dataset-audit-123", "schema": {"type": "object", "additionalProperties": true, "properties": {"__typo_result": {"type": "string"}, "__typo_record_id": {"type": "integer"}}}, "key_properties": ["__typo_record_id"], "bookmark_properties": ["__typo_record_id"]}\n' + # noqa pylint: disable=line-too-long
    '{"type": "RECORD", "stream": "tap-typo-repository-mock_repository-dataset-mock_dataset-audit-123", "record": {"date": "today", "typo": "tap", "__typo_result": "Error", "__typo_record_id": 1}}\n' + # noqa pylint: disable=line-too-long
    '{"type": "STATE", "value": {"bookmarks": {"tap-typo-repository-mock_repository-dataset-mock_dataset-audit-123": {"__typo_record_id": 1}}}}\n' + # noqa pylint: disable=line-too-long
    '{"type": "RECORD", "stream": "tap-typo-repository-mock_repository-dataset-mock_dataset-audit-123", "record": {"date": "today", "typo": "tap", "__typo_result": "OK", "__typo_record_id": 2}}\n' +  # noqa pylint: disable=line-too-long
    '{"type": "STATE", "value": {"bookmarks": {"tap-typo-repository-mock_repository-dataset-mock_dataset-audit-123": {"__typo_record_id": 2}}}}\n' + # noqa pylint: disable=line-too-long
    '{"type": "RECORD", "stream": "tap-typo-repository-mock_repository-dataset-mock_dataset-audit-123", "record": {"date": "today", "typo": "tap", "__typo_result": "Error", "__typo_record_id": 3}}\n' +  # noqa pylint: disable=line-too-long
    '{"type": "STATE", "value": {"bookmarks": {"tap-typo-repository-mock_repository-dataset-mock_dataset-audit-123": {"__typo_record_id": 3}}}}\n' + # noqa pylint: disable=line-too-long
    '{"type": "RECORD", "stream": "tap-typo-repository-mock_repository-dataset-mock_dataset-audit-123", "record": {"date": "today", "typo": "tap", "__typo_result": "OK", "__typo_record_id": 4}}\n' +  # noqa pylint: disable=line-too-long
    '{"type": "STATE", "value": {"bookmarks": {"tap-typo-repository-mock_repository-dataset-mock_dataset-audit-123": {"__typo_record_id": 4}}}}\n' # noqa pylint: disable=line-too-long
)
