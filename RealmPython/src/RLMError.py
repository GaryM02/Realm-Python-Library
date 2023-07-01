import ctypes
from realm_core import rlm_lib

class Error(ctypes.Structure):
    _fields_ = [("error", ctypes.c_int), ("message", ctypes.c_char_p),
                ("usercode_error", ctypes.c_char_p), ("kind", ctypes.c_int)]

def check_error():
    err = Error()
    rlm_lib.realm_get_last_error.argtypes = [ctypes.POINTER(Error)]
    rlm_lib.realm_get_last_error(ctypes.byref(err))
    print(err.message)