'''
    This file contains test cases for pycellfit.py file
'''

import unittest
import pycellfit.pycellfit


class TestHello(unittest.TestCase):
    """
        This class contains test cases for the functions in pycellfit/pycellfit.py
    """

    def test_hello(self):
        ans = pycellfit.pycellfit.hello()

        # Case 1
        self.assertEqual(ans, "hello new")


if __name__ == "__main__":
    unittest.main()
