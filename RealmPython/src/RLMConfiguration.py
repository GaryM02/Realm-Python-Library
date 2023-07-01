import ctypes
import RLMSchema
from realm_core import rlm_lib


class Error(ctypes.Structure):
    _fields_ = [
        ("error", ctypes.c_int),
        ("message", ctypes.c_char_p),
        ("usercode_error", ctypes.c_char_p),
        ("kind", ctypes.c_int),
    ]


def check_error():
    err = Error()
    rlm_lib.realm_get_last_error.argtypes = [ctypes.POINTER(Error)]
    rlm_lib.realm_get_last_error(ctypes.byref(err))
    print(err.message)


class configuration:
    def __init__(self):
        self.__schema__ = RLMSchema.Schema()
        self.__config_handle__ = self.get_config_handle()

        self.set_schema_version(self.__config_handle__)
        try:
            self.set_schema_object(
                self.__config_handle__, self.__schema__.__schema_handle__
            )
        except Error() as e:
            print(e.message)

        encoded_file = "default.realm".encode("utf-8")
        self.set_path_for_realm(self.__config_handle__, encoded_file)

    def get_config_handle(self):
        rlm_lib.realm_config_new.restype = ctypes.c_void_p
        return rlm_lib.realm_config_new()

    def set_schema_object(self, config_handle, schema_handle):
        rlm_lib.realm_config_set_schema.restype = ctypes.c_void_p
        return rlm_lib.realm_config_set_schema(
            ctypes.c_void_p(config_handle), ctypes.c_void_p(schema_handle)
        )

    def set_schema_version(self, config_handle):
        rlm_lib.realm_config_set_schema_version.restype = ctypes.c_void_p
        return rlm_lib.realm_config_set_schema_version(
            ctypes.c_void_p(config_handle), 1
        )

    def set_path_for_realm(self, config_handle, encoded_file):
        rlm_lib.realm_config_set_path.restype = ctypes.c_void_p
        return rlm_lib.realm_config_set_path(
            ctypes.c_void_p(config_handle), encoded_file
        )
