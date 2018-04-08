from unittest import TestCase

from differential_comparer.comparer import processApis

class ComparerTestCase(TestCase):

    def setUp(self):
        self.API_ORIGINAL = \
            '/home/farkaz00/Documents/MISO/IoT_Challenge8/03.Case_Study/03.SHAS_REST_API.json'
        self.API_TYPE_CHANGE = \
            '/home/farkaz00/Documents/MISO/IoT_Challenge8/03.Case_Study/03.SHAS_REST_API_TYPE_CHANGE.json'
        self.API_DEPRECATED_METHOD = \
            '/home/farkaz00/Documents/MISO/IoT_Challenge8/03.Case_Study/03.SHAS_REST_API_DEPRECATED_METHOD_UPDATE.json'

    def testProcessApisTypeChange(self):
        diffs = processApis(self.API_ORIGINAL, self.API_TYPE_CHANGE)
        self.assertTrue(len(diffs) > 0)
        m = map(str, diffs)

        for node in m:
            predicate = node.split(':')
            result = str(predicate[1]).strip()
            self.assertEqual(
                'expected u\'integer\', got u\'string\'',
                result 
            )
    
    def testProcessApisDeprecatedMethod(self):
        diffs = processApis(self.API_ORIGINAL, self.API_DEPRECATED_METHOD)
        self.assertTrue(len(diffs) > 0)
        m = map(str, diffs)
        container = {
            'unexpected value', 
            'expected {u\'post\'', 
            'expected {u\'get\''
        }

        for node in m:
            predicate = node.split(':')
            result = str(predicate[1]).strip()
            self.assertIn(result, container)

