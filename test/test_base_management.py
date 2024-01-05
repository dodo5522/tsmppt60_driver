import unittest
from unittest.mock import patch

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
    def _dummy_requests_get(cls, _url, timeout):
        _converted_param = str(_url).split("?")[1]
        if _converted_param in cls._dummy_table_scaling:
            _text = cls._dummy_table_scaling[_converted_param]
        else:
            _text = cls._dummy_table_response[_converted_param]
        return DummyResponse(_url, _text)

    @classmethod
    def _to_url_params(cls, modbus_register):
        addr = int(modbus_register[0])
        reg = int(modbus_register[-1])
        return "ID=1&F=4&AHI={}&ALO={}&RHI={}&RLO={}".format(
            str(addr >> 8), str(addr & 255), str(reg >> 8), str(reg & 255)
        )

    @classmethod
    @patch("tsmppt60_driver.base.requests.get", auto_spec=True)
    def setUpClass(cls, patched_get):
        cls._dummy_table_scaling = {
            cls._to_url_params(ModbusRegisterTable.VOLTAGE_SCALING): "1,4,4,0,180,0,0",
            cls._to_url_params(ModbusRegisterTable.CURRENT_SCALING): "1,4,4,0,80,0,0",
            cls._to_url_params(ModbusRegisterTable.VOLTAGE_SCALING_HIGH): "1,4,2,0,180",
            cls._to_url_params(ModbusRegisterTable.VOLTAGE_SCALING_LOW): "1,4,2,0,0",
            cls._to_url_params(ModbusRegisterTable.CURRENT_SCALING_HIGH): "1,4,2,0,80",
            cls._to_url_params(ModbusRegisterTable.CURRENT_SCALING_LOW): "1,4,2,0,0",
        }

        cls._dummy_table_response = {
            cls._to_url_params(ModbusRegisterTable.BATTERY_VOLTAGE): "1,4,2,17,160",  # 24.78515625
            cls._to_url_params(ModbusRegisterTable.CHARGING_CURRENT): "1,4,2,255,168",  # -0.21484375
            cls._to_url_params(ModbusRegisterTable.TARGET_REGULATION_VOLTAGE): "1,4,2,0,0",  # 0.0
            cls._to_url_params(ModbusRegisterTable.OUTPUT_POWER): "1,4,2,0,0",  # 0.0
            cls._to_url_params(ModbusRegisterTable.ARRAY_VOLTAGE): "1,4,2,0,84",  # 0.45
            cls._to_url_params(ModbusRegisterTable.ARRAY_CURRENT): "1,4,2,0,0",  # 0.0
            cls._to_url_params(ModbusRegisterTable.VMP_LAST_SWEEP): "1,4,2,11,208",  # 16.61
            cls._to_url_params(ModbusRegisterTable.VOC_LAST_SWEEP): "1,4,2,15,193",  # 22.15
            cls._to_url_params(ModbusRegisterTable.POWER_LAST_SWEEP): "1,4,2,0,23",  # 3.0
            cls._to_url_params(ModbusRegisterTable.HEATSINK_TEMP): "1,4,2,0,7",  # 7.0
            cls._to_url_params(ModbusRegisterTable.BATTERY_TEMP): "1,4,2,0,25",  # 25.0
            cls._to_url_params(ModbusRegisterTable.AH_CHARGE_RESETABLE): "1,4,4,0,2,231,134",  # 19034.2
            cls._to_url_params(ModbusRegisterTable.KWH_CHARGE_RESETABLE): "1,4,2,1,4",
        }  # 260.0

        patched_get.side_effect = cls._dummy_requests_get
        cls._mb = tsmppt60_driver.base.ManagementBase("dummy.co.jp")

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch("tsmppt60_driver.base.requests.get", auto_spec=True)
    def test_compute_scaler_voltage(self, patched_get):
        patched_get.side_effect = self._dummy_requests_get

        key = self._to_url_params(ModbusRegisterTable.VOLTAGE_SCALING_HIGH)
        elems = str(self._dummy_table_scaling[key]).split(",")
        high = int(elems[3]) << 8 | int(elems[4])
        # "1,4,2,0,180"

        key = self._to_url_params(ModbusRegisterTable.VOLTAGE_SCALING_LOW)
        elems = str(self._dummy_table_scaling[key]).split(",")
        low = int(elems[3]) << 8 | int(elems[4])
        # "1,4,2,0,10"

        # V_PU lo must be shifted by 16 (divided by 2^16) and then added to V_PU hi
        expected_value = float(high) + float(low) / pow(2, 16)
        v_scaled = self._mb._compute_scaler(ModbusRegisterTable.VOLTAGE_SCALING)

        self.assertEqual(expected_value, v_scaled)

    @patch("tsmppt60_driver.base.requests.get", auto_spec=True)
    def test_compute_scaler_current(self, patched_get):
        patched_get.side_effect = self._dummy_requests_get

        key = self._to_url_params(ModbusRegisterTable.CURRENT_SCALING_HIGH)
        elems = str(self._dummy_table_scaling[key]).split(",")
        high = int(elems[3]) << 8 | int(elems[4])
        # "1,4,2,0,180"

        key = self._to_url_params(ModbusRegisterTable.CURRENT_SCALING_LOW)
        elems = str(self._dummy_table_scaling[key]).split(",")
        low = int(elems[3]) << 8 | int(elems[4])
        # "1,4,2,0,10"

        # V_PU lo must be shifted by 16 (divided by 2^16) and then added to V_PU hi
        expected_value = float(high) + float(low) / pow(2, 16)
        i_scaled = self._mb._compute_scaler(ModbusRegisterTable.CURRENT_SCALING)

        self.assertEqual(expected_value, i_scaled)

    @patch("tsmppt60_driver.base.requests.get", auto_spec=True)
    def test_get_scaled_value_V(self, patched_get):
        patched_get.side_effect = self._dummy_requests_get

        modbus_register = ModbusRegisterTable.BATTERY_VOLTAGE

        val = self._mb.get_scaled_value(
            address=modbus_register[0], scale_factor=modbus_register[1], register=modbus_register[-1]
        )

        self.assertEqual(round(24.78515625, 2), val)

    @patch("tsmppt60_driver.base.requests.get", auto_spec=True)
    def test_get_scaled_value_A(self, patched_get):
        patched_get.side_effect = self._dummy_requests_get

        modbus_register = ModbusRegisterTable.CHARGING_CURRENT

        val = self._mb.get_scaled_value(
            address=modbus_register[0], scale_factor=modbus_register[1], register=modbus_register[-1]
        )

        self.assertEqual(round(-0.21484375, 2), val)

    @patch("tsmppt60_driver.base.requests.get", auto_spec=True)
    def test_get_scaled_value_W(self, patched_get):
        patched_get.side_effect = self._dummy_requests_get

        modbus_register = ModbusRegisterTable.OUTPUT_POWER

        val = self._mb.get_scaled_value(
            address=modbus_register[0], scale_factor=modbus_register[1], register=modbus_register[-1]
        )

        self.assertEqual(0.0, val)

    @patch("tsmppt60_driver.base.requests.get", auto_spec=True)
    def test_get_scaled_value_Ah(self, patched_get):
        patched_get.side_effect = self._dummy_requests_get

        modbus_register = ModbusRegisterTable.AH_CHARGE_RESETABLE

        val = self._mb.get_scaled_value(
            address=modbus_register[0], scale_factor=modbus_register[1], register=modbus_register[-1]
        )

        self.assertEqual(19034.2, val)

    @patch("tsmppt60_driver.base.requests.get", auto_spec=True)
    def test_get_scaled_value_kWh(self, patched_get):
        patched_get.side_effect = self._dummy_requests_get

        modbus_register = ModbusRegisterTable.KWH_CHARGE_RESETABLE

        val = self._mb.get_scaled_value(
            address=modbus_register[0], scale_factor=modbus_register[1], register=modbus_register[-1]
        )

        self.assertEqual(260.0, val)


if __name__ == "__main__":
    unittest.main()
