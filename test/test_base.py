#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import unittest
from tsmppt60.driver.base import Logger
from tsmppt60.driver.base import ManagementBase
from tsmppt60.driver.base import ChargeControllerStatus


class TestLogger(unittest.TestCase):
    """ Test case for base. """
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init(self):
        obj = Logger()
        self.assertTrue(hasattr(obj, "logger"))

    def test_inherit(self):
        pass


class TestManagementBase(unittest.TestCase):
    """ Test case for ManagementBase. """
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init(self):
        obj = ManagementBase()
        self.assertTrue(hasattr(obj, "_url"))


class TestChargeControllerStatus(unittest.TestCase):
    """ Test case for ChargeControllerStatus. """
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init(self):
        obj = ChargeControllerStatus()
        self.assertTrue(hasattr(obj, "_mb"))


if __name__ == "__main__":
    unittest.main()
