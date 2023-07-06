import sys, os
import unittest
sys.path.append(os.path.abspath(os.path.join('RealmPython', 'src')))
from RLMError import *


class TestError(unittest.TestCase):
    def test_check_error(self):
        # Create an instance of Error and call check_error
        try:
            error = Error()
        except AssertionError as e:
            print(e)

        try:
            check_error()
        except AssertionError as e:
            print(e)
        
