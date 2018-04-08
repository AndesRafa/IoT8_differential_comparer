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

        dif1 = diffs[0]
        self.assertEqual(dif1.api_name, 'SHAS API') 
        self.assertEqual(dif1.old_api_version, '0.0.1') 
        self.assertEqual(dif1.new_api_version, '0.0.2') 
        self.assertEqual(dif1.type, 'EXPECTED') 
        self.assertEqual(dif1.old_value, '0.0.1') 
        self.assertEqual(dif1.new_value, '0.0.2') 

        dif1 = diffs[1]
        self.assertEqual(dif1.api_name, 'SHAS API') 
        self.assertEqual(dif1.old_api_version, '0.0.1') 
        self.assertEqual(dif1.new_api_version, '0.0.2') 
        self.assertEqual(dif1.type, 'EXPECTED') 
        self.assertEqual(dif1.old_value, 'integer') 
        self.assertEqual(dif1.new_value, 'string') 

    
    def testProcessApisDeprecatedMethod(self):
        diffs = processApis(self.API_ORIGINAL, self.API_DEPRECATED_METHOD)
        self.assertTrue(len(diffs) > 0)

        dif1 = diffs[0]
        self.assertEqual(dif1.api_name, 'SHAS API') 
        self.assertEqual(dif1.old_api_version, '0.0.1') 
        self.assertEqual(dif1.new_api_version, '0.0.3') 
        self.assertEqual(dif1.type, 'EXPECTED') 
        self.assertEqual(dif1.old_value, '0.0.1') 
        self.assertEqual(dif1.new_value, '0.0.3') 

        dif2 = diffs[1]
        self.assertEqual(dif2.api_name, 'SHAS API') 
        self.assertEqual(dif2.old_api_version, '0.0.1') 
        self.assertEqual(dif2.new_api_version, '0.0.3') 
        self.assertEqual(dif2.type, 'UNEXPECTED') 
        self.assertEqual(dif2.old_value, None) 
        self.assertTrue(len(dif2.new_value)) 

        dif3 = diffs[2]
        self.assertEqual(dif3.api_name, 'SHAS API') 
        self.assertEqual(dif3.old_api_version, '0.0.1') 
        self.assertEqual(dif3.new_api_version, '0.0.3') 
        self.assertEqual(dif3.type, 'UNEXPECTED') 
        self.assertEqual(dif3.old_value, None) 
        self.assertTrue(len(dif3.new_value)) 

        dif4 = diffs[3]
        self.assertEqual(dif4.api_name, 'SHAS API') 
        self.assertEqual(dif4.old_api_version, '0.0.1') 
        self.assertEqual(dif4.new_api_version, '0.0.3') 
        self.assertEqual(dif4.type, 'EXPECTED') 
        self.assertTrue(len(dif4.old_value)) 
        self.assertEqual(dif4.new_value, None) 

