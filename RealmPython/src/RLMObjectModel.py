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
        # for attribute, default_value in cls.__dict__.items():
        #     yield {"property": attribute, "property_value": default_value}
        return ObjectModel.__subclasses__()

    def __get_no_subclasses__():
        return len(ObjectModel.__get_subclasses__())

    @staticmethod
    def __get_subclass_attributes__():
        for subcls in ObjectModel.__get_subclasses__():
            # attributes = []
            # for attribute, default_value in subcls.__dict__.items():
                
            #     attributes.append({"property": attribute, "property_value": default_value})
                
            yield (subcls.__name__, inspect.getargspec(subcls.__init__).args[1:], inspect.getargspec(subcls.__init__).defaults)
            
    @staticmethod
    def __get_rlm_schema_objects__():
        __schema_classes__ = []
        __schema_properties__ = []
        Class_Info_Arr = (Class_Info * ObjectModel.__get_no_subclasses__())()
        All_Property_Info_Arr = []
        x = 0
        for cls_name, cls_args, cls_defaults in ObjectModel.__get_subclass_attributes__():
            
            
            map_args_defaults = {}
            value_types = []

            rlm_class = Class_Info(
                f'{cls_name}'.encode('utf-8'), 
                "".encode("utf-8"), 
                ctypes.c_ulong(len(cls_args)), 
                ctypes.c_ulong(0), 
                ctypes.c_uint32(0), 
                ctypes.c_int(0)
                )
            Class_Info_Arr[x] = rlm_class
            rlm_class_properties = []

            if cls_defaults != None:
                Property_Info_Arr = (Property_Info * 20)()
                try:
                    for d in cls_defaults:
                        value_types.append(value_type(type(d)))
                except:
                    pass
                if len(cls_args) == len(cls_defaults):
                    i = 0
                    while i < len(cls_args):
                        map_args_defaults[f'{cls_args[i]}'] = value_types[i]
                        i+=1
                    
                    j=0
                    for prop in map_args_defaults:
                        
                        
                        Property_Info_Arr[j] = Property_Info(
                                    f"{prop}".encode("utf-8"),
                                    f"_{prop}".encode("utf-8"),
                                    ctypes.c_int(map_args_defaults[prop]),
                                    ctypes.c_int(0),
                                    "".encode("utf-8"),
                                    "".encode("utf-8"),
                                    ctypes.c_int64(0),
                                    ctypes.c_int(0),
                                )
                    
                    # __schema_classes__.append(rlm_class)
                    __schema_properties__.append(Property_Info_Arr)

                else:
                    raise AttributeError('Realm Error: Please ensure that all attributes have default values')
              
            else:
                raise AttributeError('Realm Error: Please ensure all objects are defined properly')
            
            x += 1  

        return Class_Info_Arr, __schema_properties__

            
            
            # if cls_defaults != None:
            #     i = 0
            #     while i <= len(cls_args):
            #         map_args_defaults[f'{cls_args[i]}'] = cls_defaults[i]
            #         i+=1

            # yield map_args_defaults