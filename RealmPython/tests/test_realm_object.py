import sys, os
import unittest

sys.path.append(os.path.abspath(os.path.join('RealmPython', 'src')))
from RLMObject import *

def convert_pyobject_value_to_realm_object_value(value):
    new_value = RealmValue()
    
    
    if isinstance(value, str):
        new_value.type = RealmValueTypeEnum.RLM_TYPE_STRING
        new_value.values.string = RealmString(
            data=value.encode("utf-8"),
            size=len(value.encode("utf-8"))
        )
    elif isinstance(value, float):
        new_value.type = RealmValueTypeEnum.RLM_TYPE_FLOAT
        new_value.values.fnum = value
    elif isinstance(value, bool):
        
        new_value.type = RealmValueTypeEnum.RLM_TYPE_BOOL
        new_value.values.boolean = value
    elif isinstance(value, int):
        
        new_value.type = RealmValueTypeEnum.RLM_TYPE_INT
        new_value.values.integer = value
    
    return new_value


class TestRealmValueConversion(unittest.TestCase):
    def test_convert_pyobject_value_to_realm_object_value_int(self):
        value = 42
        converted_value = convert_pyobject_value_to_realm_object_value(value)
        
        self.assertEqual(converted_value.type.value, RealmValueTypeEnum.RLM_TYPE_INT)
        self.assertEqual(converted_value.values.integer, value)
    
    def test_convert_pyobject_value_to_realm_object_value_str(self):
        value = "Hello World"
        converted_value = convert_pyobject_value_to_realm_object_value(value)

        self.assertEqual(converted_value.type.value, RealmValueTypeEnum.RLM_TYPE_STRING)
        self.assertEqual(converted_value.values.string.data.decode("utf-8"), value)
        self.assertEqual(converted_value.values.string.size, len(value))
    
    def test_convert_pyobject_value_to_realm_object_value_float(self):
        value = 3.14
        converted_value = convert_pyobject_value_to_realm_object_value(value)
        
        self.assertEqual(converted_value.type.value, RealmValueTypeEnum.RLM_TYPE_FLOAT)
        self.assertEqual(round(converted_value.values.fnum, 2), value)
    
    def test_convert_pyobject_value_to_realm_object_value_bool(self):
        value = True
        converted_value = convert_pyobject_value_to_realm_object_value(value)
        self.assertEqual(converted_value.type.value, RealmValueTypeEnum.RLM_TYPE_BOOL)
        self.assertEqual(converted_value.values.boolean, value)


