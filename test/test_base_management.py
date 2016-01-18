#!/usr/bin/env python
# -*- coding:utf-8 -*-

import unittest
from minimock import mock
from minimock import restore
import tsmppt60_driver
from tsmppt60_driver.base import ModbusRegisterTable


class DummyRequest:
    """Dummy request class against requests.Reguest."""

    def __init__(self, _url):
        self.url = _url


class DummyResponse:
    """Dummy response class against requests.Response."""

    def __init__(self, _url, _text):
        self.request = DummyRequest(_url)
        self.text = _text


class TestMb(unittest.TestCase):
    """Test case for ManagementBase."""

    @classmethod
    def _to_url_params(cls, modbus_register):
        addr = int(modbus_register[0])
        reg = int(modbus_register[-1])
        return 'ID=1&F=4&AHI={}&ALO={}&RHI={}&RLO={}' \
            .format(str(addr >> 8), str(addr & 255), str(reg >> 8), str(reg & 255))

    @classmethod
    def setUpClass(cls):
        def dummy_requests_get(_url, timeout):
            _converted_param = str(_url).split("?")[1]
            if _converted_param in cls._dummy_table_scaling:
                _text = cls._dummy_table_scaling[_converted_param]
            else:
                _text = cls._dummy_table_response[_converted_param]
            return DummyResponse(_url, _text)

        cls._dummy_table_scaling = {
            cls._to_url_params(ModbusRegisterTable.VOLTAGE_SCALING_HIGH): "1,4,2,1,180",
            cls._to_url_params(ModbusRegisterTable.VOLTAGE_SCALING_LOW): "1,4,2,2,10",
            cls._to_url_params(ModbusRegisterTable.CURRENT_SCALING_HIGH): "1,4,2,3,80",
            cls._to_url_params(ModbusRegisterTable.CURRENT_SCALING_LOW): "1,4,2,4,20"}

        cls._dummy_table_response = {
            cls._to_url_params(ModbusRegisterTable.BATTERY_VOLTAGE): {"raw_text": "1,4,2,16,25", "value": 22.64},
            cls._to_url_params(ModbusRegisterTable.CHARGING_CURRENT): {"raw_text": "1,4,2,255,168", "value": -0.2},
            cls._to_url_params(ModbusRegisterTable.TARGET_REGULATION_VOLTAGE): {"raw_text": "1,4,2,0,0", "value": 0.0},
            cls._to_url_params(ModbusRegisterTable.OUTPUT_POWER): {"raw_text": "1,4,2,0,0", "value": 0.0},
            cls._to_url_params(ModbusRegisterTable.ARRAY_VOLTAGE): {"raw_text": "1,4,2,0,84", "value": 0.45},
            cls._to_url_params(ModbusRegisterTable.ARRAY_CURRENT): {"raw_text": "1,4,2,0,0", "value": 0.0},
            cls._to_url_params(ModbusRegisterTable.VMP_LAST_SWEEP): {"raw_text": "1,4,2,11,208", "value": 16.61},
            cls._to_url_params(ModbusRegisterTable.VOC_LAST_SWEEP): {"raw_text": "1,4,2,15,193", "value": 22.15},
            cls._to_url_params(ModbusRegisterTable.POWER_LAST_SWEEP): {"raw_text": "1,4,2,0,23", "value": 3.0},
            cls._to_url_params(ModbusRegisterTable.HEATSINK_TEMP): {"raw_text": "1,4,2,0,7", "value": 7.0},
            cls._to_url_params(ModbusRegisterTable.BATTERY_TEMP): {"raw_text": "1,4,2,0,25", "value": 25.0},
            cls._to_url_params(ModbusRegisterTable.AH_CHARGE_RESETABLE): {"raw_text": "1,4,4,0,2,231,134", "value": 19034.2},
            cls._to_url_params(ModbusRegisterTable.KWH_CHARGE_RESETABLE): {"raw_text": "1,4,2,1,4", "value": 260.0}}

        mock("tsmppt60_driver.base.requests.get", returns_func=dummy_requests_get)

        cls._mb = tsmppt60_driver.base.ManagementBase('dummy.co.jp')

    @classmethod
    def tearDownClass(cls):
        restore()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_compute_scaler_voltage(self):
        key = self._to_url_params(ModbusRegisterTable.VOLTAGE_SCALING_HIGH)
        elems = str(self._dummy_table_scaling[key]).split(',')
        high = int(elems[3]) << 8 | int(elems[4])
        # "1,4,2,0,180"

        key = self._to_url_params(ModbusRegisterTable.VOLTAGE_SCALING_LOW)
        elems = str(self._dummy_table_scaling[key]).split(',')
        low = int(elems[3]) << 8 | int(elems[4])
        # "1,4,2,0,10"

        # V_PU lo must be shifted by 16 (divided by 2^16) and then added to V_PU hi
        expected_value = float(high) + float(low) / pow(2, 16)

        v_scaled = self._mb._compute_scaler(
            ModbusRegisterTable.VOLTAGE_SCALING_HIGH[0],
            ModbusRegisterTable.VOLTAGE_SCALING_LOW[0])

        self.assertEqual(expected_value, v_scaled)

    def test_compute_scaler_current(self):
        key = self._to_url_params(ModbusRegisterTable.CURRENT_SCALING_HIGH)
        elems = str(self._dummy_table_scaling[key]).split(',')
        high = int(elems[3]) << 8 | int(elems[4])
        # "1,4,2,0,180"

        key = self._to_url_params(ModbusRegisterTable.CURRENT_SCALING_LOW)
        elems = str(self._dummy_table_scaling[key]).split(',')
        low = int(elems[3]) << 8 | int(elems[4])
        # "1,4,2,0,10"

        # V_PU lo must be shifted by 16 (divided by 2^16) and then added to V_PU hi
        expected_value = float(high) + float(low) / pow(2, 16)

        i_scaled = self._mb._compute_scaler(
            ModbusRegisterTable.CURRENT_SCALING_HIGH[0],
            ModbusRegisterTable.CURRENT_SCALING_LOW[0])

        self.assertEqual(expected_value, i_scaled)


if __name__ == '__main__':
    unittest.main()
