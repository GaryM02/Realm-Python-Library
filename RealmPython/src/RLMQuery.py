import ctypes
from realm_core import rlm_lib
from RLMError import check_error
from RLMObject import *
import re 


class RealmQueryArg(ctypes.Structure):
    _fields_ = [
        ("nb_args", ctypes.c_size_t),               # size_t nb_args
        ("is_list", ctypes.c_bool),                 # bool is_list
        ("arg", ctypes.POINTER(RealmValue))         # realm_value_t* arg
    ]

def __get_all_realm_results__(realm_handle, class_key):
    rlm_lib.realm_object_find_all.restype = ctypes.c_void_p
    res = rlm_lib.realm_object_find_all(ctypes.c_void_p(realm_handle), ctypes.c_uint32(class_key))
    if res != None:
        return res
    else:
        check_error()

def __get_object_key__(realm_object_handle):
    rlm_lib.realm_object_get_key.restype = ctypes.c_void_p
    res = rlm_lib.realm_object_get_key(ctypes.c_void_p(realm_object_handle))
    if res != None:
        return res
    else:
        check_error()

def __get_object_get_table__(realm_object_handle):
    rlm_lib.realm_object_get_table.restype = ctypes.c_void_p
    res = rlm_lib.realm_object_get_table(ctypes.c_void_p(realm_object_handle))
    if res != None:
        return res
    else:
        check_error() 

"""
filter
"""
def __num_args__(query_string):
    query_string = query_string.split('&&')
    return len(query_string)

def __new_arg_arr__(query_string):
    num_args = __num_args__(query_string)
    arg_arr_t = (RealmQueryArg * num_args)()
    args = re.split('==|<=|>=|<|>|!=|&&', query_string)
    args = [args[x].strip() for x in range(1, len(args), 2)]
    for idx, s in enumerate(args):
        s = args[idx]
        if (s.find('-') <= 0) and s.replace('-', '', 1).isdigit():
            if (args[idx].count('-') == 0):
                args[idx] = int(args[idx])
                args[idx] = convert_pyobject_value_to_realm_object_value(args[idx])
            else:
                args[idx] = int(args[idx])
                args[idx] = convert_pyobject_value_to_realm_object_value(args[idx])
                
        elif (s.find('-') <= 0) and (s.count('.') < 2) and \
            (s.replace('-', '', 1).replace('.', '', 1).isdigit()):
            if (args[idx].count('-') == 0):
                args[idx] = float(args[idx])
                args[idx] = convert_pyobject_value_to_realm_object_value(args[idx])
            else:
                args[idx] = float(args[idx])
                args[idx] = convert_pyobject_value_to_realm_object_value(args[idx])
        else:
            args[idx] = args[idx][1:-1]
            args[idx] = convert_pyobject_value_to_realm_object_value(args[idx])

        arg_arr_t[idx] = RealmQueryArg(1, False, ctypes.pointer(args[idx]))
    
    return arg_arr_t

def __parse_query_for_results__(realm_results_t, query_string):
    num_args = __num_args__(query_string)
    arg_t_arr = __new_arg_arr__(query_string)
    rlm_lib.realm_query_parse_for_results.restype = ctypes.c_void_p
    res = rlm_lib.realm_query_parse_for_results(ctypes.c_void_p(realm_results_t), ctypes.c_char_p(query_string.encode('utf-8')), ctypes.c_size_t(num_args), ctypes.byref(arg_t_arr))
    if res != None:
        return res
    else:
        check_error()

def __realm_query_get_description__(realm_query_t):
    rlm_lib.realm_query_get_description.restype = ctypes.c_char_p
    res = rlm_lib.realm_query_get_description(ctypes.c_void_p(realm_query_t))
    if res != None:
        return res 
    else:
        check_error()

def __realm_query_find_first__(realm_query_t):
    out_value = (RealmValue * 5)()
    out_found = ctypes.c_bool()
    rlm_lib.realm_query_find_first.restype = ctypes.c_bool
    res = rlm_lib.realm_query_find_first(ctypes.c_void_p(realm_query_t), ctypes.byref(out_value), ctypes.byref(out_found))
    if res == True:
        return out_value
    else:
        check_error()

def __get_num_objects__(realm_handle, class_key):
    out_count = ctypes.c_size_t()
    rlm_lib.realm_get_num_objects.restype = ctypes.c_bool
    res = rlm_lib.realm_get_num_objects(ctypes.c_void_p(realm_handle), ctypes.c_uint32(class_key), ctypes.byref(out_count))
    if res == True:
        return out_count
    else:
        check_error()

def __count_num_results__(results_handle):
    out_count = ctypes.c_size_t()
    rlm_lib.realm_results_count.restype = ctypes.c_bool
    res = rlm_lib.realm_results_count(ctypes.c_void_p(results_handle), ctypes.byref(out_count))
    if res == True:
        return out_count
    else:
        check_error()

def __get_objects_from_results__(results_handle, index_of_object):
    rlm_lib.realm_results_get_object.restype = ctypes.c_void_p
    return rlm_lib.realm_results_get_object(ctypes.c_void_p(results_handle), ctypes.c_size_t(index_of_object))

def __realm_object_to_string__(object_handle):
    rlm_lib.realm_object_to_string.restype = ctypes.c_char_p
    res = rlm_lib.realm_object_to_string(ctypes.c_void_p(object_handle))
    return res

def __realm_get_new_results_handle__(old_results_handle, query_t_handle):
    rlm_lib.realm_results_filter.restype = ctypes.c_void_p
    res = rlm_lib.realm_results_filter(ctypes.c_void_p(old_results_handle), ctypes.c_void_p(query_t_handle))
    if res != None:
        return res
    else:
        check_error()