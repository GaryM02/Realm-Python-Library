import ctypes
import RLMConfiguration
from realm_core import rlm_lib

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
        check_error()
