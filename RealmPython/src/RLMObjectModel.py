import ctypes
import inspect

# Realm Structures
class Class_Info(ctypes.Structure):
    _fields_ = [
        ("name", ctypes.c_char_p),
        ("primary_key", ctypes.c_char_p),
        ("num_properties", ctypes.c_size_t),
        ("num_computed_properties", ctypes.c_size_t),
        ("key", ctypes.c_uint32),
        ("flags", ctypes.c_int),
    ]

class Property_Info(ctypes.Structure):
    _fields_ = [
        ("name", ctypes.c_char_p),
        ("public_name", ctypes.c_char_p),
        ("type", ctypes.c_int),
        ("collection_type", ctypes.c_int),
        ("link_target", ctypes.c_char_p),
        ("link_origin_property_name", ctypes.c_char_p),
        ("key", ctypes.c_int64),
        ("flags", ctypes.c_int),
    ]

def value_type(value):
    value = value
    if value == int:
        return 0
    elif value == bool:
        return 1
    elif value == str:
        return 2
    elif value == float:
        return 9




"""
RLMObjectModel
ObjectModel - native python object inherit objectmodel and in doing so subclasses are found and attributes are taken
to create a schema of that native object.
no class is yet instanciated
"""
"""
RlmSchema will call object model functions to set the schema 
"""
class ObjectModel:
    """
    ObjectModel - return -> subclass __init__ attributes and defaults
    """

    @staticmethod
    def __get_subclasses__():
        return ObjectModel.__subclasses__()

    def __get_no_subclasses__():
        return len(ObjectModel.__get_subclasses__())

    @staticmethod
    def __get_subclass_attributes__():
        for subcls in ObjectModel.__get_subclasses__():
            yield (subcls.__name__, inspect.getargspec(subcls.__init__).args[1:], inspect.getargspec(subcls.__init__).defaults)
            
    @staticmethod
    def __get_rlm_schema_objects__():
        __schema_classes__ = []
        __schema_properties__ = []

        Class_Info_Arr = (Class_Info * ObjectModel.__get_no_subclasses__())()
        x = 0
        max_no_properties = 0
        for cls_name, cls_args, cls_defaults in ObjectModel.__get_subclass_attributes__():
            Class_Info_Arr[x] = Class_Info(
                f'{cls_name}'.encode('utf-8'), 
                ''.encode("utf-8"), 
                ctypes.c_ulong(len(cls_args)), 
                ctypes.c_ulong(0), 
                ctypes.c_uint32(0), 
                ctypes.c_int(0)
                )
            
            if len(cls_args) > max_no_properties:
                max_no_properties = len(cls_args)
            
            if cls_defaults != None:
                sub_arr = (Property_Info * len(cls_args))
                props_sub_arr = sub_arr()
                for i in range(len(cls_args)):
                    props_sub_arr[i] = Property_Info(
                                    f"{cls_args[i]}".encode("utf-8"),
                                    "".encode("utf-8"),
                                    ctypes.c_int(value_type(type(cls_defaults[i]))),
                                    ctypes.c_int(0),
                                    "".encode("utf-8"),
                                    "".encode("utf-8"),
                                    ctypes.c_int64(0),
                                    ctypes.c_int(0),
                                )
                __schema_properties__.append(ctypes.pointer(props_sub_arr))
               
            else:
                raise AttributeError('Realm Error: Please ensure all objects are defined properly')
            x += 1

        all_props_arr = (ctypes.POINTER(sub_arr) * len(__schema_properties__))()

        cast_array = (Property_Info * max_no_properties)
        for i in range(len(__schema_properties__)):
            all_props_arr[i] = ctypes.cast(__schema_properties__[i], ctypes.POINTER(cast_array))
        return Class_Info_Arr, all_props_arr

            
        