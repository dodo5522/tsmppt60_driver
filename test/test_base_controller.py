#!/usr/bin/env python
# -*- coding:utf-8 -*-

import unittest
try:
    from unittest.mock import patch
except:
    from mock import patch
from tsmppt60_driver.base import ModbusRegisterTable
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
    def _requests_get(cls, url, timeout):

        def _url_parm(modbus_registers):
            addr_hi = str(int(modbus_registers[0]) >> 8)
            addr_lo = str(int(modbus_registers[0]) & 255)
            reg_hi = str(int(modbus_registers[-1]) >> 8)
            reg_lo = str(int(modbus_registers[-1]) & 255)

            return 'ID=1&F=4&AHI={}&ALO={}&RHI={}&RLO={}' \
                .format(addr_hi, addr_lo, reg_hi, reg_lo)

        table_scaling = {
            _url_parm(ModbusRegisterTable.VOLTAGE_SCALING_HIGH): "1,4,2,0,180",
            _url_parm(ModbusRegisterTable.VOLTAGE_SCALING_LOW): "1,4,2,0,0",
            _url_parm(ModbusRegisterTable.CURRENT_SCALING_HIGH): "1,4,2,0,80",
            _url_parm(ModbusRegisterTable.CURRENT_SCALING_LOW): "1,4,2,0,0",
            _url_parm(ModbusRegisterTable.BATTERY_VOLTAGE): "1,4,2,17,160"}  # 24.78515625

        text = table_scaling[str(url).split("?")[-1]]
        return DummyResponse(url, text)

    @classmethod
    @patch("tsmppt60_driver.base.requests.get", auto_spec=True)
    def setUpClass(cls, patched_get):
        patched_get.side_effect = cls._requests_get

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
        expected_value = {
            "group": "Battery",
            "label": "Battery Voltage",
            "value": 24.78515625,
            "unit": "V"}

        patched_get.side_effect = self._requests_get

        value = self._bat.get_status(38, 'V', 'Battery Voltage', 1)

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
