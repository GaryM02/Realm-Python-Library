import unittest
from test_dll_imports import TestDLLImport
from test_object_model import TestRealmStructures
from test_realm_configuration import TestConfiguration
from test_realm_error import TestError
from test_realm_instance import TestRealm
from test_realm_object import TestRealmValueConversion
from test_realm_schema import TestSchema

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestDLLImport))
    
    runner = unittest.TextTestRunner()
    print(runner.run(suite))

def test_suite_2():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSchema))
    
    runner = unittest.TextTestRunner()
    print(runner.run(suite))

def test_suite_3():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestConfiguration))
    
    runner = unittest.TextTestRunner()
    print(runner.run(suite))

def test_suite_4():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestRealmStructures))
    
    
    runner = unittest.TextTestRunner()
    print(runner.run(suite))

def test_suite_5():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestError))
    
    runner = unittest.TextTestRunner()
    print(runner.run(suite))

def test_suite_6():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestRealm))
   
    
    runner = unittest.TextTestRunner()
    print(runner.run(suite))

def test_suite_7():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestRealmValueConversion))
    
    runner = unittest.TextTestRunner()
    print(runner.run(suite))



test_suite()
test_suite_2()
test_suite_3()
test_suite_4()
test_suite_5()
test_suite_6()
test_suite_7()