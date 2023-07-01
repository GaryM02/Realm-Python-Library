import os
import ctypes

path = os.path.dirname(__file__)
# Load the dylib file
libname = os.path.join(path, "librealm-ffi-dbg.dylib") 

rlm_lib = ctypes.cdll.LoadLibrary(libname)