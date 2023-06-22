import ctypes
import RLMConfiguration
from realm_core import rlm_lib
from RLMObjectModel import Class_Info, Property_Info
from RLMObject import get_values_from_instance

class Error(ctypes.Structure):
    _fields_ = [("error", ctypes.c_int), ("message", ctypes.c_char_p),
                ("usercode_error", ctypes.c_char_p), ("kind", ctypes.c_int)]

def check_error():
    err = Error()
    rlm_lib.realm_get_last_error.argtypes = [ctypes.POINTER(Error)]
    rlm_lib.realm_get_last_error(ctypes.byref(err))
    print(err.message)

class Realm:
    def __init__(self):
        self.__rlm_configuration__ = RLMConfiguration.configuration()
        
        rlm_lib.realm_open.restype = ctypes.c_void_p
        self.realm_handle = rlm_lib.realm_open(ctypes.c_void_p(self.__rlm_configuration__.__config_handle__))
        
    def __get_num_classes__(self):
        rlm_lib.realm_get_num_classes.restype = ctypes.c_size_t
        return rlm_lib.realm_get_num_classes(ctypes.c_void_p(self.realm_handle))

    def __get_class_keys__(self):
        num_classes = self.__get_num_classes__()
        key_arr = (ctypes.c_uint32 * num_classes)()
        actual_num_classes_returned = ctypes.c_size_t()
        rlm_lib.realm_get_class_keys.restype = ctypes.c_bool
        res = rlm_lib.realm_get_class_keys(ctypes.c_void_p(self.realm_handle), ctypes.byref(key_arr), ctypes.c_size_t(num_classes), ctypes.byref(actual_num_classes_returned))
        if res == True:
            return key_arr
        else:
            raise OSError('Could not get class keys')
    
    def __find_class_with_key__(self, class_key):
        class_info_buff = Class_Info()
        rlm_lib.realm_get_class.restype = ctypes.c_bool
        res = rlm_lib.realm_get_class(ctypes.c_void_p(self.realm_handle), ctypes.c_uint32(class_key), ctypes.byref(class_info_buff))
        if res == True:
            return class_info_buff
        else:
            check_error()

    def __get_class_key_by_name__(self, class_name):
        class_info_buff = Class_Info()
        out_found = ctypes.c_bool()
        rlm_lib.realm_find_class.restype = ctypes.c_bool
        res = rlm_lib.realm_find_class(ctypes.c_void_p(self.realm_handle), f'{class_name}'.encode('utf-8'), ctypes.byref(out_found), ctypes.byref(class_info_buff))
        if res == True:
            return class_info_buff.key
        else:
            check_error()

    def __get_property_keys__(self, class_key):
        class_info = self.__find_class_with_key__(class_key)

        num_properties = class_info.num_properties
        out_col_keys = (ctypes.c_int64 * num_properties)()
        max_num_keys = num_properties
        actual_num_keys = ctypes.c_size_t()
        rlm_lib.realm_get_property_keys.restype = ctypes.c_bool
        res = rlm_lib.realm_get_property_keys(ctypes.c_void_p(self.realm_handle), ctypes.c_uint32(class_key), ctypes.byref(out_col_keys), ctypes.c_size_t(max_num_keys), ctypes.byref(actual_num_keys))
        if res == True:
            return out_col_keys
        else:
            check_error()

    """
    objects
    """
    def __get_num_objects__(self, class_key):
        out_count = ctypes.c_size_t()
        rlm_lib.realm_get_num_objects.restype = ctypes.c_bool
        res = rlm_lib.realm_get_num_objects(ctypes.c_void_p(self.realm_handle), ctypes.c_uint32(class_key), ctypes.byref(out_count))
        if res == True:
            return out_count
        else:
            raise OSError('Could not get class objects')

    def __realm_object_create__(self, class_key):
        rlm_lib.realm_object_create.restype = ctypes.c_void_p
        return rlm_lib.realm_object_create(ctypes.c_void_p(self.realm_handle), ctypes.c_uint32(class_key))

    def __realm_object_create_with_primary_key__(self):
        pass

    def __set_values_of_properties__(self, class_key, values, property_keys):
        new_obj_handle = self.__realm_object_create__(class_key)
        # properties = self.__get_property_keys__(class_key)
        num_values = len(property_keys)
        is_default = False
        
        rlm_lib.realm_set_values.restype = ctypes.c_bool
        res = rlm_lib.realm_set_values(ctypes.c_void_p(new_obj_handle), ctypes.c_size_t(num_values), ctypes.byref(property_keys), ctypes.byref(values), ctypes.c_bool(is_default))
        if res == True:
            return res
        else:
            check_error()

    

    """
    transaction control
    """
    def __begin_write__(self):
        rlm_lib.realm_begin_write.restype = ctypes.c_bool
        return rlm_lib.realm_begin_write(ctypes.c_void_p(self.realm_handle))
    
    def __commit_write__(self):
        rlm_lib.realm_commit.restype = ctypes.c_bool
        return rlm_lib.realm_commit(ctypes.c_void_p(self.realm_handle))
    
    def __rollback_transaction__(self):
        """
        for testing
        """
        rlm_lib.realm_rollback.restype = ctypes.c_bool
        res = rlm_lib.realm_rollback(ctypes.c_void_p(self.realm_handle))
        if res == True:
            return res
        else:
            check_error()

        """
        add

        takes in a pyobject instance, gets it's values, converts them
        to RealmValue, generates an array of values, gets class key by class name,
        begins write transaction, sets new values of properties, commits write and 
        returns
        """

    def add(self, py_object_instance):
        class_key = self.__get_class_key_by_name__(py_object_instance.__class__.__name__)
        property_keys = self.__get_property_keys__(class_key)
        values_arr = get_values_from_instance(py_object_instance, len(property_keys))
        writing = self.__begin_write__()
        if writing == True:
            self.__set_values_of_properties__(class_key, values_arr, property_keys)
            commited = self.__commit_write__()
            if commited == False:
                raise OSError('Could not commit data')
