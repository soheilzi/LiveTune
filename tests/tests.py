#incomplete

import unittest
import time
import threading
import socket

from LiveTune import initVar  # Replace 'your_module' with the actual module name containing the initVar class


class TestInitVar(unittest.TestCase):

    def test_initialization(self):
        var = initVar(10, 8000)
        self.assertEqual(var.var_value, 10)

    def test_arithmetic_operations(self):
        var1 = initVar(10, 8001)
        var2 = initVar(20, 8002)

        # Test addition
        result_add = var1 + var2
        self.assertEqual(result_add.var_value, 30)

        # Test subtraction
        result_sub = var2 - var1
        self.assertEqual(result_sub.var_value, 10)

        # Test multiplication
        result_mul = var1 * var2
        self.assertEqual(result_mul.var_value, 200)

        # Test division
        result_div = var2 / var1
        self.assertEqual(result_div.var_value, 2)

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

    
if __name__ == '__main__':
    unittest.main()
