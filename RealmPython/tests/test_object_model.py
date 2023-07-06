


import sys, os

import unittest
import ctypes

sys.path.append(os.path.abspath(os.path.join('RealmPython', 'src')))

from RLMObjectModel import *

class PersonDemo(ObjectModel):
    def __init__(self, name='', age=0):
        self.name = name
        self.age = age

class TestRealmStructures(unittest.TestCase):
    def test_class_info_structure(self):
        class_info = Class_Info(
                        name=b"Dummy Class",
                        primary_key=b"Dummy Primary Key",
                        num_properties=5,
                        num_computed_properties=2,
                        key=123,
                        flags=0
                    )
        
        # Verify the fields of the Class_Info structure
        self.assertTrue(hasattr(class_info, 'name'))
        self.assertTrue(hasattr(class_info, 'primary_key'))
        self.assertTrue(hasattr(class_info, 'num_properties'))
        self.assertTrue(hasattr(class_info, 'num_computed_properties'))
        self.assertTrue(hasattr(class_info, 'key'))
        self.assertTrue(hasattr(class_info, 'flags'))
        
        # Verify the types of the fields
        self.assertIsInstance(class_info.name, bytes)
        self.assertIsInstance(class_info.primary_key, bytes)
        self.assertIsInstance(class_info.num_properties, int)
        self.assertIsInstance(class_info.num_computed_properties, int)
        self.assertIsInstance(class_info.key, int)
        self.assertIsInstance(class_info.flags, int)
    
    def test_property_info_structure(self):
        property_info = Property_Info(
                            name=b"Dummy Property",
                            public_name=b"Dummy Public Name",
                            type=0,
                            collection_type=1,
                            link_target=b"Dummy Link Target",
                            link_origin_property_name=b"Dummy Origin Property",
                            key=456,
                            flags=0
                        )
        
        # Verify the fields of the Property_Info structure
        self.assertTrue(hasattr(property_info, 'name'))
        self.assertTrue(hasattr(property_info, 'public_name'))
        self.assertTrue(hasattr(property_info, 'type'))
        self.assertTrue(hasattr(property_info, 'collection_type'))
        self.assertTrue(hasattr(property_info, 'link_target'))
        self.assertTrue(hasattr(property_info, 'link_origin_property_name'))
        self.assertTrue(hasattr(property_info, 'key'))
        self.assertTrue(hasattr(property_info, 'flags'))
        
        # Verify the types of the fields
        self.assertIsInstance(property_info.name, bytes)
        self.assertIsInstance(property_info.public_name, bytes)
        self.assertIsInstance(property_info.type, int)
        self.assertIsInstance(property_info.collection_type, int)
        self.assertIsInstance(property_info.link_target, bytes)
        self.assertIsInstance(property_info.link_origin_property_name, bytes)
        self.assertIsInstance(property_info.key, int)
        self.assertIsInstance(property_info.flags, int)
    
    def test_value_type_function(self):
        # Verify the return values for different value types
        self.assertEqual(value_type(int), 0)
        self.assertEqual(value_type(bool), 1)
        self.assertEqual(value_type(str), 2)
        self.assertEqual(value_type(float), 9)
    
    def test_object_model_subclasses(self):
        # Verify that ObjectModel returns the correct subclasses
        subclasses = ObjectModel.__get_subclasses__()
        
        # Replace SubClass1 and SubClass2 with the actual subclasses in your code
        self.assertIsNotNone(subclasses)
        
    def test_object_model_subclass_attributes(self):
        # Verify that ObjectModel returns the correct subclass attributes
        subclass_attributes = list(ObjectModel.__get_subclass_attributes__())
        
        # Replace SubClass1 and SubClass2 with the actual subclasses in your code
        self.assertEqual(subclass_attributes, [
            ('PersonDemo', ['name', 'age'], ('', 0)),
        ])
    
    def test_object_model_rlm_schema_objects(self):
        # Verify that ObjectModel returns the correct RLM schema objects
        class_info, properties = ObjectModel.__get_rlm_schema_objects__()
        
        # Replace the expected values based on your code logic
        self.assertIsNotNone(class_info)
        self.assertIsNotNone(properties)
        self.assertIsInstance(class_info, ctypes.Array)
        self.assertIsInstance(properties, ctypes.Array)

