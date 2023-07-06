import numpy
import ctypes
import RLMConfiguration
from realm_core import rlm_lib
from RLMObjectModel import Class_Info, Property_Info
from RLMObject import get_values_from_instance, get_values_from_kwargs
import RLMQuery as RQ
import json
from RLMObject import RealmValue, RealmString, RealmValueTypeEnum


class Error(ctypes.Structure):
    _fields_ = [
        ("error", ctypes.c_int),
        ("message", ctypes.c_char_p),
        ("usercode_error", ctypes.c_char_p),
        ("kind", ctypes.c_int),
    ]


def check_error():
    err = Error()
    rlm_lib.realm_get_last_error(ctypes.byref(err))
    print(str(err.message))


class Realm:
    def __init__(self):
        self.__rlm_configuration__ = RLMConfiguration.configuration()

        rlm_lib.realm_open.restype = ctypes.c_void_p
        self.realm_handle = rlm_lib.realm_open(
            ctypes.c_void_p(self.__rlm_configuration__.__config_handle__)
        )
        self.__path_to_realm__ = self.__get_path_for_realm__(
            self.__rlm_configuration__.__config_handle__
        )

    def __get_path_for_realm__(self, config_handle):
        rlm_lib.realm_config_get_path.restype = ctypes.c_char_p
        res = rlm_lib.realm_config_get_path(ctypes.c_void_p(config_handle))
        if res != None:
            return res
        else:
            check_error()

    def __get_num_classes__(self):
        rlm_lib.realm_get_num_classes.restype = ctypes.c_size_t
        return rlm_lib.realm_get_num_classes(ctypes.c_void_p(self.realm_handle))

    def __get_class_keys__(self):
        num_classes = self.__get_num_classes__()
        key_arr = (ctypes.c_uint32 * num_classes)()
        actual_num_classes_returned = ctypes.c_size_t()
        rlm_lib.realm_get_class_keys.restype = ctypes.c_bool
        res = rlm_lib.realm_get_class_keys(
            ctypes.c_void_p(self.realm_handle),
            ctypes.byref(key_arr),
            ctypes.c_size_t(num_classes),
            ctypes.byref(actual_num_classes_returned),
        )
        if res == True:
            return key_arr
        else:
            raise OSError("Could not get class keys")

    def __find_class_with_key__(self, class_key):
        class_info_buff = Class_Info()
        rlm_lib.realm_get_class.restype = ctypes.c_bool
        res = rlm_lib.realm_get_class(
            ctypes.c_void_p(self.realm_handle),
            ctypes.c_uint32(class_key),
            ctypes.byref(class_info_buff),
        )
        if res == True:
            return class_info_buff
        else:
            check_error()

    def __get_class_key_by_name__(self, class_name, realm_handle):
        class_info_buff = Class_Info()
        out_found = ctypes.c_bool()
        rlm_lib.realm_find_class.restype = ctypes.c_bool
        res = rlm_lib.realm_find_class(
            ctypes.c_void_p(realm_handle),
            f"{class_name}".encode("utf-8"),
            ctypes.byref(out_found),
            ctypes.byref(class_info_buff),
        )
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
        res = rlm_lib.realm_get_property_keys(
            ctypes.c_void_p(self.realm_handle),
            ctypes.c_uint32(class_key),
            ctypes.byref(out_col_keys),
            ctypes.c_size_t(max_num_keys),
            ctypes.byref(actual_num_keys),
        )
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
        res = rlm_lib.realm_get_num_objects(
            ctypes.c_void_p(self.realm_handle),
            ctypes.c_uint32(class_key),
            ctypes.byref(out_count),
        )
        if res == True:
            return out_count
        else:
            raise OSError("Could not get class objects")

    def __realm_object_create__(self, class_key):
        rlm_lib.realm_object_create.restype = ctypes.c_void_p
        return rlm_lib.realm_object_create(
            ctypes.c_void_p(self.realm_handle), ctypes.c_uint32(class_key)
        )

    def __realm_object_create_with_primary_key__(self):
        pass

    def __set_values_of_properties__(self, class_key, values, property_keys):
        new_obj_handle = self.__realm_object_create__(class_key)
        # properties = self.__get_property_keys__(class_key)
        num_values = len(property_keys)
        is_default = False

        rlm_lib.realm_set_values.restype = ctypes.c_bool
        res = rlm_lib.realm_set_values(
            ctypes.c_void_p(new_obj_handle),
            ctypes.c_size_t(num_values),
            ctypes.byref(property_keys),
            ctypes.byref(values),
            ctypes.c_bool(is_default),
        )
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

    def __realm_begin_read__(self):
        rlm_lib.realm_begin_read.restype = ctypes.c_bool
        res = rlm_lib.realm_begin_read(ctypes.c_void_p(self.realm_handle))
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
        class_key = self.__get_class_key_by_name__(
            py_object_instance.__class__.__name__, self.realm_handle
        )
        property_keys = self.__get_property_keys__(class_key)
        values_arr = get_values_from_instance(py_object_instance, len(property_keys))
        writing = self.__begin_write__()
        if writing == True:
            self.__set_values_of_properties__(class_key, values_arr, property_keys)
            commited = self.__commit_write__()
            if commited == False:
                raise OSError("Could not commit data")

    def objects(self, py_object_model):
        """
        Adding objects as a class allows us to instanciate a new
        list of objects from results.
        We can add all of our query methods (filter methods) within
        this class.
        """
        rlm_handle = self.realm_handle
        rlm = self

        class Objects:
            def __init__(self, py_object_model, realm_handle):
                self.class_key = rlm.__get_class_key_by_name__(
                    py_object_model.__name__, realm_handle
                )
                self.realm_handle = realm_handle
                self.object_model = py_object_model
                self.results_handle = self.__get_all_results_handle__(
                    py_object_model, realm_handle
                )
                self.__objects__ = self.objects(self.results_handle)

            """
            Queries
            """

            def __get_all_results_handle__(self, py_object_model, realm_handle):
                return RQ.__get_all_realm_results__(realm_handle, self.class_key)

            def objects(self, results_handle):
                """
                objects

                objects:
                 -takes our results handle,
                 -loops our num objects in the result,
                 -gets an object handle at index <index>,
                 -converts our binary string to python string,
                 -loads the json inside of our string,
                 -appends the json to the objects list
                """
                objects = []
                num_objects = RQ.__count_num_results__(results_handle).value

                for i in range(num_objects):
                    object_handle = RQ.__get_objects_from_results__(results_handle, i)
                    objects.append(
                        json.loads(
                            RQ.__realm_object_to_string__(object_handle).decode("utf-8")
                        )
                    )
                return objects

            def object_handles(self, results_handle):
                """
                object_handles

                object_handles:
                 -takes our results handle,
                 -loops our num objects in the result,
                 -gets an object handle at index <index>,
                 -appends the object handle to the objects list

                 -similar to above method but will be used for
                 updating objects
                """
                objects = []
                num_objects = RQ.__count_num_results__(results_handle).value

                for i in range(num_objects):
                    object_handle = RQ.__get_objects_from_results__(results_handle, i)
                    objects.append(object_handle)
                return objects

            def filter(self, realm_query_string):
                filtered_query_handle = RQ.__parse_query_for_results__(
                    self.results_handle, realm_query_string
                )
                new_results_handle = RQ.__realm_get_new_results_handle__(
                    self.results_handle, filtered_query_handle
                )
                return self.objects(new_results_handle)

            def filter_for_update(self, realm_query_string, **kwargs):
                """
                filter_for_update

                filter_for_update:
                 -take in query and get object handles,
                 -use kwargs to find property and get it's key
                 -use kwarg value to create new RealmValue
                 -update property at <key> to new <RealmValue>
                """
                keys = rlm.__get_property_keys__(self.class_key)

                prop_keys = (ctypes.c_uint64 * len(kwargs))()
                for idx, prop_name in enumerate(kwargs.keys()):
                    prop_keys[idx] = RQ.__realm_find_property__(
                        rlm_handle, self.class_key, prop_name
                    )

                values = get_values_from_kwargs(kwargs, len(kwargs))

                filtered_query_handle = RQ.__parse_query_for_results__(
                    self.results_handle, realm_query_string
                )
                new_results_handle = RQ.__realm_get_new_results_handle__(
                    self.results_handle, filtered_query_handle
                )
                object_handles = self.object_handles(new_results_handle)
                for handle in object_handles:
                    is_default = False
                    rlm.__begin_write__()
                    rlm_lib.realm_set_values.restype = ctypes.c_bool
                    res = rlm_lib.realm_set_values(
                        ctypes.c_void_p(handle),
                        ctypes.c_size_t(len(kwargs)),
                        ctypes.byref(prop_keys),
                        ctypes.byref(values),
                        ctypes.c_bool(is_default),
                    )
                    if res == True:
                        rlm.__commit_write__()
                    else:
                        check_error()

            def delete_all(self):
                rlm.__begin_write__()
                rlm_lib.realm_results_delete_all.restype = ctypes.c_bool
                res = rlm_lib.realm_results_delete_all(
                    ctypes.c_void_p(self.results_handle)
                )
                if res == True:
                    rlm.__commit_write__()
                    return res
                else:
                    check_error()

            def delete(self, realm_query_string):
                filtered_query_handle = RQ.__parse_query_for_results__(
                    self.results_handle, realm_query_string
                )
                new_results_handle = RQ.__realm_get_new_results_handle__(
                    self.results_handle, filtered_query_handle
                )
                rlm.__begin_write__()
                rlm_lib.realm_results_delete_all.restype = ctypes.c_bool
                res = rlm_lib.realm_results_delete_all(
                    ctypes.c_void_p(new_results_handle)
                )
                if res == True:
                    rlm.__commit_write__()
                    return res
                else:
                    check_error()

        return Objects(py_object_model, rlm_handle)

    def delete_realm(self):
        """
        This will delete all realm files associated with the realm instance
        """
        try:
            rlm_lib.realm_close.restype = ctypes.c_bool
            res = rlm_lib.realm_close(ctypes.c_void_p(self.realm_handle))
            
            if res == True:
                out_deleted = ctypes.c_bool()
                rlm_lib.realm_delete_files.restype = ctypes.c_bool
                res = rlm_lib.realm_delete_files(
                    ctypes.c_char_p(self.__path_to_realm__), ctypes.byref(out_deleted)
                )
                if res == True:
                    return res
                else:
                    check_error()
            else:
                check_error()
        except RuntimeError as e:
            print(str(e.message))
