import ctypes
import RLMObjectModel
from realm_core import rlm_lib


class Error(ctypes.Structure):
    _fields_ = [("error", ctypes.c_int), ("message", ctypes.c_char_p),
                ("usercode_error", ctypes.c_char_p), ("kind", ctypes.c_int)]



class Schema:

    def __init__(self):
        self.__objects__ =[obj for obj in RLMObjectModel.ObjectModel.__get_rlm_schema_objects__()] 
        self.__schema_handle__ = self.get_schema_handle()
        

    def get_schema_handle(self):
        classes = self.__objects__[0]
        properties = self.__objects__[1]
   
        rlm_lib.realm_schema_new.restype = ctypes.c_void_p
        
        return rlm_lib.realm_schema_new(ctypes.byref(classes), ctypes.c_size_t(len(classes)), ctypes.byref(properties))
       
