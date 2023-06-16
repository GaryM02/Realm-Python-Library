import ctypes

import RLMObjectModel
from realm_core import rlm_lib
from RLMObjectModel import Class_Info, ObjectModel, Property_Info

class Error(ctypes.Structure):
    _fields_ = [("error", ctypes.c_int), ("message", ctypes.c_char_p),
                ("usercode_error", ctypes.c_char_p), ("kind", ctypes.c_int)]

def check_error():
    err = Error()
    rlm_lib.realm_get_last_error.argtypes = [ctypes.POINTER(Error)]
    rlm_lib.realm_get_last_error(ctypes.byref(err))
    print(err.message)

class Schema:

    def __init__(self):
        self.__objects__ =[obj for obj in RLMObjectModel.ObjectModel.__get_rlm_schema_objects__()] 
        self.__schema_handle__ = self.get_schema_handle()
        check_error()

    def get_schema_handle(self):
        classes = self.__objects__[0]
        properties = self.__objects__[1]
        print(classes, properties)
        Property_Info_Arr = (Property_Info * 20)
        All_props_arr = (Property_Info_Arr * len(properties))
        Class_Info_Arr = (Class_Info * ObjectModel.__get_no_subclasses__())
        all_p_arr = All_props_arr()
        i = 0
        while i < len(properties):
            all_p_arr[i] = properties[i]
            # All_props_arr[idx] = prop
            i+=1


        # rlm_lib.realm_schema_new.argtypes = [
        #     ctypes.POINTER(Class_Info_Arr),
        #     ctypes.c_size_t,
        #     ctypes.POINTER(All_props_arr),
        # ]
        # rlm_lib.realm_schema_new.restype = ctypes.c_void_p

                        

        # return rlm_lib.realm_schema_new(classes, 0, all_p_arr)
        """
        this is a temporary change to figure out why we cant add more than one class
        """
        arr = (ctypes.POINTER(Property_Info) * 10)
        rlm_lib.realm_schema_new.argtypes = [
            ctypes.POINTER(Class_Info),
            ctypes.c_size_t,
            ctypes.POINTER(arr),
        ]
        rlm_lib.realm_schema_new.restype = ctypes.c_void_p

        clasarr = (Class_Info * 2)

        clas = clasarr(
            Class_Info(
                'test5'.encode('utf-8'), 
                "".encode("utf-8"), 
                ctypes.c_ulong(1), 
                ctypes.c_ulong(0), 
                ctypes.c_uint32(0), 
                ctypes.c_int(0)
                ), 
            Class_Info(
                'test4'.encode('utf-8'), 
                "".encode("utf-8"), 
                ctypes.c_ulong(1), 
                ctypes.c_ulong(0), 
                ctypes.c_uint32(0), 
                ctypes.c_int(0)
                )
            )
        proparray = arr(
            ctypes.pointer(Property_Info(
                "hat".encode("utf-8"),
                "".encode("utf-8"),
                ctypes.c_int(2),
                ctypes.c_int(0),
                "".encode("utf-8"),
                "".encode("utf-8"),
                ctypes.c_int64(0),
                ctypes.c_int(0),
            ))
        )

        return rlm_lib.realm_schema_new(clas, 1, proparray)
