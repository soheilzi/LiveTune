import unittest
import time
import threading
import socket
import os

# from LiveTune import liveVar
from LiveTune.liveVar import liveVar
from LiveTune.tools.tune import typeChecker
from LiveTune.liveTrigger import liveTrigger

class TestLiveTune(unittest.TestCase):

    def test_initialization_liveVar(self):
        var = liveVar(10, 'a')
        self.assertEqual(var(), 10, "liveVar test failed")
        self.assertEqual(var.var_value, 10, "liveVar test failed")
        self.assertEqual(var.dtype, int, "liveVar test failed")
        self.assertEqual(var.tag, 'a', "liveVar test failed")

    def test_initialization_liveTrigger(self):
        var = liveTrigger('b')
        self.assertEqual(var.tag, 'b', "liveTrigger test failed")
        self.assertEqual(var(), False, "liveTrigger test failed")
        

    def test_arithmetic_operations(self):
        var1 = liveVar(10, 'c')
        var2 = liveVar(20, 'd')

        # Test addition
        result_add = var1 + var2
        self.assertEqual(result_add, 30, "Add test failed")

        # Test subtraction
        result_sub = var2 - var1
        self.assertEqual(result_sub, 10, "Sub test failed")

        # Test multiplication
        result_mul = var1 * var2
        self.assertEqual(result_mul, 200, "Multiplication test failed")

        # Test division
        result_div = var2 / var1
        self.assertEqual(result_div, 2, "Division test failed")

        # Test division by zero
        with self.assertRaises(ZeroDivisionError):
            _ = var1 / liveVar(0, 'z')

    def test_get_set_item(self):
        var = liveVar(5, 'e')
        self.assertEqual(var['value'], 5)
        var['value'] = 15
        self.assertEqual(var['value'], 15)

        # Test invalid key for __getitem__
        with self.assertRaises(KeyError):
            _ = var['invalid_key']

        # Test invalid key for __setitem__
        with self.assertRaises(KeyError):
            var['invalid_key'] = 25

    def test_thread_safety(self):
        var = liveVar(0, 'f')

        def increase_var_value():
            for _ in range(1000):
                with var.lock:
                    var.var_value += 1

        threads = [threading.Thread(target=increase_var_value) for _ in range(10)]
        for t in threads:
            t.start()

        for t in threads:
            t.join()

        self.assertEqual(var.var_value, 10000)

    def test_invalid_var_value_type(self):
        # Test invalid type for var_value
        with self.assertRaises(TypeError):
            _ = liveVar("invalid_value", "g")

    def test_invalid_tag_type(self):
        # Test invalid type for tag
        with self.assertRaises(TypeError):
            _ = liveVar(10, 3)

    def test_string_representation(self):
        var = liveVar(42, "h") 
        self.assertEqual(str(var), "42")

    def test_inequality_operators(self):
        var1 = liveVar(10, "i")
        var2 = liveVar(20, "j")
        var3 = liveVar(10, "k")

        self.assertTrue(var1 == var3)
        self.assertTrue(var1 != var2)

    def test_inplace_arithmetic_operations(self):
        var = liveVar(5, "l")
        var += 3
        self.assertEqual(var.var_value, 8, "Inplace addition test failed")

        var -= 2
        self.assertEqual(var.var_value, 6, "Inplace subtraction test failed")

        var *= 5
        self.assertEqual(var.var_value, 30, "Inplace multiplication test failed")

        var /= 3
        self.assertEqual(var.var_value, 10, "Inplace division test failed")

    def test_invalid_operations(self):
        var = liveVar(10, "m")

        # Test invalid operation with None
        with self.assertRaises(TypeError):
            _ = var + None

        # Test invalid operation with string
        with self.assertRaises(TypeError):
            _ = var - "invalid"

        # Test invalid operation with list
        with self.assertRaises(TypeError):
            _ = var * [1, 2, 3]

    def test_edge_cases(self):
        # Test large var_value
        var = liveVar(2 ** 32, "n")
        self.assertEqual(var.var_value, 2 ** 32)

    def test_duplicate_port_usage(self):
        # Test duplicate port usage
        var1 = liveVar(10, "o")
        try:
            time.sleep(1)
            var2 = liveVar(20, "o")
        except Exception as e:
            self.assertIn("Error binding to port 8014", str(e))

    def test_typeChecker(self):
        # Test invalid type for var_value
        self.assertEqual(typeChecker("True"), "bool", "Expected 'bool' but got something else")
        self.assertEqual(typeChecker("False"), "bool", "Expected 'bool' but got something else")
        self.assertEqual(typeChecker("1"), "int", "Expected 'int' but got something else")
        self.assertEqual(typeChecker("0"), "int", "Expected 'int' but got something else")
        self.assertEqual(typeChecker("-1"), "int", "Expected 'int' but got something else")
        self.assertEqual(typeChecker("1.0"), "float", "Expected 'float' but got something else")
        self.assertEqual(typeChecker("0.0"), "float", "Expected 'float' but got something else")
        self.assertEqual(typeChecker("burger"), "string", "Expected 'string' but got something else")

    def test_update(self):
        # Assuming liveVar() function is already defined and var.var_value is set to 10
        var = liveVar(10, "p")
        # Run the 'tune' command in the terminal

        port = var.dictionary_port[0]
        try:
            print(os.system(f'python3 src/LiveTune/tools/tune.py --value 5 --tag p --port {port}'))
            time.sleep(1)
        except Exception as e:
            self.fail(f"Command execution failed with error: {e}")
        
        # Now check if var.var_value has been updated to 5
        self.assertEqual(var.var_value, 5)

        #test negative integer
        try:
            print(os.system(f'python3 src/LiveTune/tools/tune.py --value -5 --tag p --port {port}'))
            time.sleep(1)
        except Exception as e:
            self.fail(f"Command execution failed with error: {e}")

        self.assertEqual(var.var_value, -5)

    def test_multiple_update(self):
        # Assuming liveVar() function is already defined and var.var_value is set to 10
        var = liveVar(10, "p2")
        # Run the 'tune' command in the terminal

        port = var.dictionary_port[0]
        try:
            print(os.system(f'python3 src/LiveTune/tools/tune.py --value 5 --tag p2 --port {port}'))
            time.sleep(1)
        except Exception as e:
            self.fail(f"Command execution failed with error: {e}")
        
        # Now check if var.var_value has been updated to 5
        self.assertEqual(var.var_value, 5)

        #test negative integer
        try:
            print(os.system(f'python3 src/LiveTune/tools/tune.py --value -5 --tag p2 --port {port}'))
            time.sleep(1)
        except Exception as e:
            self.fail(f"Command execution failed with error: {e}")

        self.assertEqual(var.var_value, -5)

    # test update but with boolean
    def test_update_bool(self):
        var = liveVar(True, "q")
        # Run the 'tune' command in the terminal

        port = var.dictionary_port[0]
        try:
            print(os.system(f'python3 src/LiveTune/tools/tune.py --value False --tag q --port {port}'))
            time.sleep(1)
        except Exception as e:
            self.fail(f"Command execution failed with error: {e}")
        
        # Now check if var.var_value has been updated to 5
        self.assertEqual(var.var_value, False, "Expected 'False' but got something else")

    # test update but with float
    def test_update_float(self):
        # Assuming liveVar() function is already defined and var.var_value is set to 10
        var = liveVar(10.0, "r")
        # Run the 'tune' command in the terminal

        port = var.dictionary_port[0]
        try:
            print(os.system(f'python3 src/LiveTune/tools/tune.py --value 5.0 --tag r --port {port}'))
            time.sleep(1)
        except Exception as e:
            self.fail(f"Command execution failed with error: {e}")
        
        # Now check if var.var_value has been updated to 5
        self.assertEqual(var.var_value, 5.0)

    def test_trigger(self):
        var = liveTrigger("s")
        self.assertEqual(var(), False, "Trigger test failed")
        port = var.dictionary_port[0]
        try:
            print(os.system(f'python3 src/LiveTune/tools/tune.py --trigger --tag s --port {port}'))
            time.sleep(1)
        except Exception as e:
            self.fail(f"Command execution failed with error: {e}")
        self.assertEqual(var(), True, "Trigger test failed")
        self.assertEqual(var(), False, "Trigger test failed")


if __name__ == '__main__':
    unittest.main()
