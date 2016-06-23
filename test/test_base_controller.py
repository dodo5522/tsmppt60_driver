#!/usr/bin/env python
# -*- coding:utf-8 -*-

import unittest
try:
    from unittest.mock import patch
except:
    from mock import patch
from tsmppt60_driver.base import ManagementBase
from tsmppt60_driver.status import BatteryStatus
from tsmppt60_driver.status import SolarArrayStatus
from tsmppt60_driver.status import TemperaturesStatus
from tsmppt60_driver.status import CountersStatus


class DummyRequest:
    """Dummy request class against requests.Reguest."""

    def __init__(self, _url):
        self.url = _url


class DummyResponse:
    """Dummy response class against requests.Response."""

    def __init__(self, _url, _text):
        self.request = DummyRequest(_url)
        self.text = _text


class TestChargeControllerStatus(unittest.TestCase):
    """ Test case for ChargeControllerStatus. """

    @classmethod
    def _gen_url_parm(cls, addr, reg):
        return 'ID=1&F=4&AHI={}&ALO={}&RHI={}&RLO={}' \
            .format(addr >> 8, addr & 255, reg >> 8, reg & 255)

    @classmethod
    @patch("tsmppt60_driver.base.requests.get", auto_spec=True)
    def setUpClass(cls, patched_get):
        def _requests_get(url, timeout):
            mb_url_parm = str(url).split("?")[-1]

            table_scaling = {
                cls._gen_url_parm(0x0000, 1): "1,4,2,0,180",  # VOLTAGE_SCALING_HIGH
                cls._gen_url_parm(0x0001, 1): "1,4,2,0,0",    # VOLTAGE_SCALING_LOW
                cls._gen_url_parm(0x0002, 1): "1,4,2,0,80",   # CURRENT_SCALING_HIGH
                cls._gen_url_parm(0x0003, 1): "1,4,2,0,0"}    # CURRENT_SCALING_LOW

            text = table_scaling[mb_url_parm]
            return DummyResponse(url, text)

        patched_get.side_effect = _requests_get

        mb = ManagementBase("dummy.uribou.mydns.jp")
        cls._bat = BatteryStatus(mb)
        cls._panel = SolarArrayStatus(mb)
        cls._temp = TemperaturesStatus(mb)
        cls._count = CountersStatus(mb)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch("tsmppt60_driver.base.requests.get", auto_spec=True)
    def test_get_battery_voltage(self, patched_get):
        def _requests_get(url, timeout):
            mb_url_parm = str(url).split("?")[-1]

            table_scaling = {
                self._gen_url_parm(0x0026, 1): "1,4,2,17,160"}  # BATTERY_VOLTAGE, 24.78515625

            text = table_scaling[mb_url_parm]
            return DummyResponse(url, text)

        patched_get.side_effect = _requests_get

        expected_value = {
            "group": "Battery",
            "label": "Battery Voltage",
            "value": 24.78515625,
            "unit": "V"}

        value = self._bat.get_status(0x0026, 'V', 'Battery Voltage', 1)

        self.assertEqual(set(expected_value.items()), set(value.items()))

        # (51, 'V', 'Target Voltage', 1)
        # (39, 'A', 'Charge Current', 1)
        # (58, 'W', 'Output Power', 1)

    @patch("tsmppt60_driver.base.requests.get", auto_spec=True)
    def test_get_target_voltage(self, patched_get):
        patched_get.return_value = "1,4,2,0,0"  # 0.0

    @patch("tsmppt60_driver.base.requests.get", auto_spec=True)
    def test_get_output_power(self, patched_get):
        patched_get.return_value = "1,4,2,0,0"  # 0.0

    @patch("tsmppt60_driver.base.requests.get", auto_spec=True)
    def test_get_battery_temperature(self, patched_get):
        patched_get.return_value = "1,4,2,0,25"  # 25.0


if __name__ == "__main__":
    unittest.main(verbosity=2)
