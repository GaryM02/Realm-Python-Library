import sys, os
import unittest
sys.path.append(os.path.abspath(os.path.join('RealmPython', 'src')))
from RLMConfiguration import *




class TestConfiguration(unittest.TestCase):
    def test_get_config_handle(self):
        config = configuration()
        config_handle = config.get_config_handle()

        self.assertIsInstance(config_handle, int)

    def test_set_schema_object(self):
        config = configuration()
        config_handle = config.get_config_handle()
        schema_handle = config.__schema__.__schema_handle__

        result = config.set_schema_object(config_handle, schema_handle)

        self.assertIsInstance(result, int)

    def test_set_schema_version(self):
        config = configuration()
        config_handle = config.get_config_handle()

        result = config.set_schema_version(config_handle)

        self.assertIsInstance(result, int)

    def test_set_path_for_realm(self):
        config = configuration()
        config_handle = config.get_config_handle()
        encoded_file = "default.realm".encode("utf-8")

        result = config.set_path_for_realm(config_handle, encoded_file)

        self.assertIsInstance(result, int)


