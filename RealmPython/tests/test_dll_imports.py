import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join('RealmPython', 'src')))

import realm_core

class TestDLLImport(unittest.TestCase):
    def test_dll_import(self):
        lib = realm_core.rlm_lib
        try:
            # If the DLL is successfully imported, the following line will not raise an exception
            self.assertIsNotNone(lib)
        except OSError:
            # If the DLL import fails, this assertion will fail
            self.fail("Failed to import the DLL.")

