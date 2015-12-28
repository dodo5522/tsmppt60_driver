#!/usr/bin/env python3
# -*- coding:utf-8 -*-

""" This script is to test this package. """

import unittest

if __name__ == "__main__":
    all_tests = unittest.TestLoader().discover("./", "test_*.py")
    unittest.TextTestRunner(verbosity=1).run(all_tests)