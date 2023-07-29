import unittest
import time
import threading
import socket
import os

# from LiveTune import initVar
from LiveTune.initVar import initVar

class TestInitVar(unittest.TestCase):

    def test_initialization(self):
        var = initVar(10, 8000)
        self.assertEqual(var.var_value, 10, "Init test failed")
        

    def test_arithmetic_operations(self):
        var1 = initVar(10, 8001)
        var2 = initVar(20, 8002)

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
            _ = var1 / initVar(0, 8003)

    def test_get_set_item(self):
        var = initVar(5, 8004)
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
        var = initVar(0, 8005)

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
            _ = initVar("invalid_value", 8006)

    def test_invalid_port_type(self):
        # Test invalid type for port
        with self.assertRaises(TypeError):
            _ = initVar(10, "invalid_port")

    def test_string_representation(self):
        var = initVar(42, 8007) 
        self.assertEqual(str(var), "42")

    def test_inequality_operators(self):
        var1 = initVar(10, 8008)
        var2 = initVar(20, 8009)
        var3 = initVar(10, 8010)

        self.assertTrue(var1 == var3)
        self.assertTrue(var1 != var2)

    def test_inplace_arithmetic_operations(self):
        var = initVar(5, 8011)
        var += 3
        self.assertEqual(var.var_value, 8, "Inplace addition test failed")

        var -= 2
        self.assertEqual(var.var_value, 6, "Inplace subtraction test failed")

        var *= 5
        self.assertEqual(var.var_value, 30, "Inplace multiplication test failed")

        var /= 3
        self.assertEqual(var.var_value, 10, "Inplace division test failed")

    def test_invalid_operations(self):
        var = initVar(10, 8012)

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
        var = initVar(2 ** 32, 8013)
        self.assertEqual(var.var_value, 2 ** 32)

    def test_duplicate_port_usage(self):
        # Test duplicate port usage
        var1 = initVar(10, 8014)
        try:
            var2 = initVar(20, 8014)
        except Exception as e:
            self.assertIn("Error binding to port 8014", str(e))

    def test_invalid_port_number(self):
        # Test invalid port number
        with self.assertRaises(ValueError):
            _ = initVar(10, -1)

    # def test_multiple_changes

    def test_update(self):
        # Assuming initVar() function is already defined and var.var_value is set to 10
        var = initVar(10, 8015)
        # Run the 'updateVar' command in the terminal
        try:
            time.sleep(1)
            print(os.system('updateVar 5 8015'))
            time.sleep(1)
        except Exception as e:
            self.fail(f"Command execution failed with error: {e}")
        
        # Now check if var.var_value has been updated to 5
        self.assertEqual(var.var_value, 5)

if __name__ == '__main__':
    unittest.main()