import unittest
import sys, os
import ctypes
sys.path.append(os.path.abspath(os.path.join('RealmPython', 'src')))
from Realm import *





class TestRealm(unittest.TestCase):
    realm = Realm()

    def test_a_open(self):
        self.assertIsNotNone(self.realm.realm_handle)

    def test_b_get_num_classes(self):
        num_classes = self.realm.__get_num_classes__()
        self.assertIsInstance(num_classes, int)

    def test_c_get_class_keys(self):
        class_keys = self.realm.__get_class_keys__()
        self.assertIsNotNone(class_keys)
        for key in class_keys:
            self.assertIsInstance(key, int)

    def test_d_find_class_with_key(self):
        class_key = 1  # Modify with a valid class key
        class_info = self.realm.__find_class_with_key__(class_key)
        self.assertIsNotNone(class_info)

    def test_e_get_class_key_by_name(self):
        class_name = "PersonDemo"  # Modify with a valid class name
        class_key = self.realm.__get_class_key_by_name__(class_name, self.realm.realm_handle)
        self.assertIsNotNone(class_key)

    def test_f_get_property_keys(self):
        class_key = 1  # Modify with a valid class key
        property_keys = self.realm.__get_property_keys__(class_key)
        self.assertIsNotNone(property_keys)
        for key in property_keys:
            self.assertIsInstance(key, int)

    def test_g_get_num_objects(self):
        class_key = 1  # Modify with a valid class key
        num_objects = self.realm.__get_num_objects__(class_key)
        self.assertIsInstance(num_objects, ctypes.c_ulong)

    def test_h_delete_realm(self):
        self.assertTrue(self.realm.delete_realm())
        
            

    

