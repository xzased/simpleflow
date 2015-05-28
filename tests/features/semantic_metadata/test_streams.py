import unittest

from cdf.core.metadata.constants import RENDERING, FIELD_RIGHTS
from cdf.metadata.url.url_metadata import (
    DIFF_QUANTITATIVE,
    DIFF_QUALITATIVE,
    ES_LIST
)
from cdf.features.semantic_metadata.streams import (
    _get_duplicate_document_mapping
)


class TestGetDuplicateDocumentMapping(unittest.TestCase):
    def test_nominal_case(self):
        metadata_list = ["title"]
        duplicate_type = "foo_duplicate"
        order_seed = 100
        actual_result = _get_duplicate_document_mapping(
            metadata_list,
            duplicate_type,
            False,
            order_seed
        )
        expected_result = {
            'metadata.title.foo_duplicate.nb': {
                'type': 'integer',
                'verbose_name': 'No. of Duplicate Title (Among All URLs)',
                'settings': {
                    'es:doc_values',
                    'agg:categorical',
                    'agg:numerical',
                    FIELD_RIGHTS.FILTERS,
                    FIELD_RIGHTS.SELECT,
                    DIFF_QUANTITATIVE
                }
            },
            'metadata.title.foo_duplicate.is_first': {
                'type': 'boolean',
                'verbose_name':
                '1st Duplicate Title Found (Among All URLs)',
                'settings': {
                    FIELD_RIGHTS.SELECT,
                    FIELD_RIGHTS.FILTERS,
                    DIFF_QUALITATIVE
                }
            },
            'metadata.title.foo_duplicate.urls': {
                'type': 'integer',
                'verbose_name': 'Sample of URLs with the Same Title (Among All URLs)',
                'settings': {
                    'es:no_index',
                    'url_id',
                    ES_LIST,
                    RENDERING.URL_STATUS,
                    FIELD_RIGHTS.SELECT
                }
            },
            'metadata.title.foo_duplicate.urls_exists': {
                'default_value': None, 'type': 'boolean'
            }
        }
        self.assertEqual(expected_result, actual_result)
