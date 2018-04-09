import json
from unittest import TestCase

from differential_comparer.differential import Differential


class DifferentialTestCaset(TestCase):

    def setUp(self):
        self.api_name = 'TEST API'
        self.old_api_version = '1.0.0'
        self.new_api_version = '2.0.0'
        self.diff_type_change = None
        #self.diff_type_change = json.loads('{'\
        #            + '\"path\":\"[\'paths\'][\'/fire_report/{id}\']'\
        #                + '[\'get\'][\'responses\'][\'200\'][\'content\']'\
        #                + '[\'application/json\'][\'schema\'][\'properties\']'\
        #                + '[\'measureDate\'][\'type\']\",' \
        #            + '\"message\": \"expected \'integer\', got'\
        #                + '\'string\'\"}')


    #def testDifferentialData(self):
    #    diff = Differential(
    #                api_name=self.api_name,
    #                old_api_version=self.old_api_version,
    #                new_api_version=self.new_api_version,
    #                diff=self.diff_type_change,
    #            )

    #    self.assertEqual(diff.api_name, self.api_name)
    #    self.assertEqual(diff.old_api_version, self.old_api_version)
    #    self.assertEqual(diff.new_api_version, self.new_api_version)
    #    self.assertEqual(diff.type, 'EXPECTED')
    #    self.assertEqual(diff.old_value, 'integer')
    #    self.assertEqual(diff.new_value, 'string')
