import sys, os

import unittest

sys.path.append(os.path.abspath(os.path.join('RealmPython', 'src')))

from RLMSchema import Schema





class TestSchema(unittest.TestCase):
    def test_schema_initialization(self):
        schema = Schema()
        
        # Verify that the __objects__ attribute is populated correctly
        self.assertIsNotNone(schema.__objects__)
        self.assertIsInstance(schema.__objects__, list)
        
        # Verify that the __schema_handle__ attribute is obtained correctly
        self.assertIsNotNone(schema.__schema_handle__)
        self.assertIs(type(schema.__schema_handle__), int)
        
