import unittest2 as unittest
from recensio.policy.patches import mangleQuery


class TestSearch(unittest.TestCase):

    def test_mangleQuery_non_ascii(self):
        keywords = {
            'Subject': {
                u'operator': u'and',
                'query': ['B\xc3\xa4rtige Fl\xc3\xb6\xc3\x9fer',
                          'F\xc3\xa4hrmann',
                          ]
            },
        }
        mangleQuery(keywords, None, None)
