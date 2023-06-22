import ctypes

class RealmValueTypeEnum(ctypes.c_int):
    RLM_TYPE_NULL = 0
    RLM_TYPE_INT = 1
    RLM_TYPE_BOOL = 2
    RLM_TYPE_STRING = 3
    RLM_TYPE_BINARY = 4
    RLM_TYPE_TIMESTAMP = 5
    RLM_TYPE_FLOAT = 6
    RLM_TYPE_DOUBLE = 7
    RLM_TYPE_DECIMAL128 = 8
    RLM_TYPE_OBJECT_ID = 9
    RLM_TYPE_LINK = 10
    RLM_TYPE_UUID = 11

# Structure definition for realm_string_t
class RealmString(ctypes.Structure):
    _fields_ = [
        ("data", ctypes.c_char_p),   # const char* data
        ("size", ctypes.c_size_t)    # size_t size
    ]

# Structure definition for realm_binary_t
class RealmBinary(ctypes.Structure):
    _fields_ = [
        ("data", ctypes.POINTER(ctypes.c_uint8)),   # const uint8_t* data
        ("size", ctypes.c_size_t)                    # size_t size
    ]

# Structure definition for realm_timestamp_t
class RealmTimestamp(ctypes.Structure):
    _fields_ = [
        ("seconds", ctypes.c_int64),   # int64_t seconds
        ("nanoseconds", ctypes.c_int32)   # int32_t nanoseconds
    ]

# Structure definition for realm_decimal128_t
class RealmDecimal128(ctypes.Structure):
    _fields_ = [
        ("w", ctypes.c_uint64 * 2)   # uint64_t w[2]
    ]

# Structure definition for realm_link_t
class RealmLink(ctypes.Structure):
    _fields_ = [
        ("target_table", ctypes.c_int),   # realm_class_key_t target_table
        ("target", ctypes.c_int)          # realm_object_key_t target
    ]

# Structure definition for realm_object_id_t
class RealmObjectId(ctypes.Structure):
    _fields_ = [
        ("bytes", ctypes.c_uint8 * 12)   # uint8_t bytes[12]
    ]

# Structure definition for realm_uuid_t
class RealmUuid(ctypes.Structure):
    _fields_ = [
        ("bytes", ctypes.c_uint8 * 16)   # uint8_t bytes[16]
    ]

# Structure definition for realm_value_t
class RealmValue(ctypes.Structure):
    class ValueUnion(ctypes.Union):
        _fields_ = [
            ("integer", ctypes.c_int64),             # int64_t integer
            ("boolean", ctypes.c_bool),              # bool boolean
            ("string", RealmString),                 # realm_string_t string
            ("binary", RealmBinary),                 # realm_binary_t binary
            ("timestamp", RealmTimestamp),           # realm_timestamp_t timestamp
            ("fnum", ctypes.c_float),                # float fnum
            ("dnum", ctypes.c_double),               # double dnum
            ("decimal128", RealmDecimal128),         # realm_decimal128_t decimal128
            ("object_id", RealmObjectId),            # realm_object_id_t object_id
            ("uuid", RealmUuid),                     # realm_uuid_t uuid
            ("link", RealmLink),                     # realm_link_t link
            ("data", ctypes.c_char * 16)              # char data[16]
        ]

    _fields_ = [
        ("values", ValueUnion),                   # Union member values
        ("type", RealmValueTypeEnum)              # realm_value_type_e type
    ]

"""get values from instance 
convert to realm datatypes
add to array of RealmValues"""




def convert_pyobject_value_to_realm_object_value(value):
    if type(value) == int:
        new_value = RealmValue()
        new_value.type = RealmValueTypeEnum.RLM_TYPE_INT
        new_value.values.integer = value
        
        return new_value
    elif type(value) == str:
        new_value = RealmValue()
        new_value.type = RealmValueTypeEnum.RLM_TYPE_STRING
        new_string = RealmString()
        new_string.data = f'{value}'.encode('utf-8')  # Use the appropriate string data
        new_string.size = len(new_string.data)
        new_value.values.string = new_string
        print(new_value)
        return new_value
    elif type(value) == float:
        new_value = RealmValue()
        new_value.type = RealmValueTypeEnum.RLM_TYPE_FLOAT
        new_value.values.fnum = value
        return new_value


def get_values_from_instance(py_object_instance, num_properties):
    values_arr = (RealmValue * num_properties)()
    i = 0
    for arg, value in py_object_instance.__dict__.items():
        """
        convert the value
        """
        print(value)
        values_arr[i] = convert_pyobject_value_to_realm_object_value(value)
        i += 1

    return values_arr