#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import tsmppt60_driver
from tsmppt60_driver.base import ModbusRegisterTable
import unittest
from minimock import mock, Mock, restore


def _convert_to_url_params(modbus_register):
    addr = int(modbus_register[0])
    reg = int(modbus_register[-1])
    return 'ID=1&F=4&AHI={}&ALO={}&RHI={}&RLO={}' \
        .format(str(addr >> 8), str(addr & 255), str(reg >> 8), str(reg & 255))


_modbus_dummy_scaling_table = {
    _convert_to_url_params(ModbusRegisterTable.VOLTAGE_SCALING_HIGH): "1,4,2,0,180",
    _convert_to_url_params(ModbusRegisterTable.VOLTAGE_SCALING_LOW): "1,4,2,0,10",
    _convert_to_url_params(ModbusRegisterTable.CURRENT_SCALING_HIGH): "1,4,2,0,80",
    _convert_to_url_params(ModbusRegisterTable.CURRENT_SCALING_LOW): "1,4,2,0,0"}

_modbus_dummy_response_table = {
    _convert_to_url_params(ModbusRegisterTable.BATTERY_VOLTAGE): {"raw_text": "1,4,2,16,25", "value": 22.64},
    _convert_to_url_params(ModbusRegisterTable.CHARGING_CURRENT): {"raw_text": "1,4,2,255,168", "value": -0.2},
    _convert_to_url_params(ModbusRegisterTable.TARGET_REGULATION_VOLTAGE): {"raw_text": "1,4,2,0,0", "value": 0.0},
    _convert_to_url_params(ModbusRegisterTable.OUTPUT_POWER): {"raw_text": "1,4,2,0,0", "value": 0.0},
    _convert_to_url_params(ModbusRegisterTable.ARRAY_VOLTAGE): {"raw_text": "1,4,2,0,84", "value": 0.45},
    _convert_to_url_params(ModbusRegisterTable.ARRAY_CURRENT): {"raw_text": "1,4,2,0,0", "value": 0.0},
    _convert_to_url_params(ModbusRegisterTable.VMP_LAST_SWEEP): {"raw_text": "1,4,2,11,208", "value": 16.61},
    _convert_to_url_params(ModbusRegisterTable.VOC_LAST_SWEEP): {"raw_text": "1,4,2,15,193", "value": 22.15},
    _convert_to_url_params(ModbusRegisterTable.POWER_LAST_SWEEP): {"raw_text": "1,4,2,0,23", "value": 3.0},
    _convert_to_url_params(ModbusRegisterTable.HEATSINK_TEMP): {"raw_text": "1,4,2,0,7", "value": 7.0},
    _convert_to_url_params(ModbusRegisterTable.BATTERY_TEMP): {"raw_text": "1,4,2,0,25", "value": 25.0},
    _convert_to_url_params(ModbusRegisterTable.AH_CHARGE_RESETABLE): {"raw_text": "1,4,4,0,2,231,134", "value": 19034.2},
    _convert_to_url_params(ModbusRegisterTable.KWH_CHARGE_RESETABLE): {"raw_text": "1,4,2,1,4", "value": 260.0}}


class DummyRequest:
    """
    Dummy request class against requests.Reguest.
    """
    def __init__(self, _url):
        self.url = _url


class DummyResponse:
    """
    Dummy response class against requests.Response.
    """
    def __init__(self, _url, _text):
        self.request = DummyRequest(_url)
        self.text = _text


def dummy_requests_get(_url, timeout):
    """
    Dummy get function against requests.get().
    """
    _converted_param = str(_url).split("?")[1]

    if _converted_param in _modbus_dummy_scaling_table:
        _text = _modbus_dummy_scaling_table[_converted_param]
    else:
        _text = _modbus_dummy_response_table[_converted_param]

    return DummyResponse(_url, _text)


class TestManagementBase(unittest.TestCase):
    """
    Test case for ManagementBase.
    """
    @classmethod
    def setUpClass(cls):
        tsmppt60_driver.base.requests.get = Mock(
                "tsmppt60_driver.base.requests.get",
                returns_func=dummy_requests_get)
        cls._mb = tsmppt60_driver.base.ManagementBase("192.168.2.1")

    @classmethod
    def tearDownClass(cls):
        restore()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_compute_scaler_voltage(self):
        v_hi = self._mb._get(addr=0x0000, reg=1)
        v_lo = self._mb._get(addr=0x0001, reg=1)
        print(v_hi)
        print(v_lo)

    def test_compute_scaler_current(self):
        c_hi = self._mb._get(addr=0x0002, reg=1)
        c_lo = self._mb._get(addr=0x0003, reg=1)
        print(c_hi)
        print(c_lo)

if __name__ == '__main__':
    unittest.main()