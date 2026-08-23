import unittest
from unittest.mock import patch

from tsmppt60_driver.base import ManagementBase
from tsmppt60_driver.hal import Register, RegisterMap


class DummyResponse:
    """Dummy response class against http.client.HTTPResponse."""

    status = 200

    def __init__(self, text):
        self._text = text

    def read(self):
        return self._text.encode("ASCII")


class DummyConnection:
    """Dummy connection class against http.client.HTTPConnection."""

    def __init__(self, responses):
        self._responses = responses
        self._path = ""

    def request(self, method, path):
        if method != "GET":
            raise AssertionError(f"Unexpected HTTP method: {method}")
        self._path = path

    def getresponse(self):
        query = self._path.split("?", maxsplit=1)[1]
        return DummyResponse(self._responses[query])


class TestMb(unittest.TestCase):
    """Test case for ManagementBase."""

    @classmethod
    def _to_url_params(cls, modbus_register: Register):
        addr = int(modbus_register.address)
        reg = int(modbus_register.registers)
        return "ID=1&F=4&AHI={}&ALO={}&RHI={}&RLO={}".format(
            str(addr >> 8), str(addr & 255), str(reg >> 8), str(reg & 255)
        )

    @classmethod
    @patch("tsmppt60_driver.base.HTTPConnection")
    def setUpClass(cls, patched_connection):
        cls._dummy_table_scaling = {
            cls._to_url_params(RegisterMap.VOLTAGE_SCALING): "1,4,4,0,180,0,0",
            cls._to_url_params(RegisterMap.CURRENT_SCALING): "1,4,4,0,80,0,0",
        }

        cls._dummy_table_response = {
            cls._to_url_params(RegisterMap.BATTERY_VOLTAGE): "1,4,2,17,160",  # 24.78515625
            cls._to_url_params(RegisterMap.CHARGING_CURRENT): "1,4,2,255,168",  # -0.21484375
            cls._to_url_params(RegisterMap.TARGET_REGULATION_VOLTAGE): "1,4,2,0,0",  # 0.0
            cls._to_url_params(RegisterMap.OUTPUT_POWER): "1,4,2,0,0",  # 0.0
            cls._to_url_params(RegisterMap.ARRAY_VOLTAGE): "1,4,2,0,84",  # 0.45
            cls._to_url_params(RegisterMap.ARRAY_CURRENT): "1,4,2,0,0",  # 0.0
            cls._to_url_params(RegisterMap.VMP_LAST_SWEEP): "1,4,2,11,208",  # 16.61
            cls._to_url_params(RegisterMap.VOC_LAST_SWEEP): "1,4,2,15,193",  # 22.15
            cls._to_url_params(RegisterMap.POWER_LAST_SWEEP): "1,4,2,0,23",  # 3.0
            cls._to_url_params(RegisterMap.HEATSINK_TEMP): "1,4,2,0,7",  # 7.0
            cls._to_url_params(RegisterMap.BATTERY_TEMP): "1,4,2,0,25",  # 25.0
            cls._to_url_params(RegisterMap.AH_CHARGE_RESETABLE): "1,4,4,0,2,231,134",  # 19034.2
            cls._to_url_params(RegisterMap.KWH_CHARGE_RESETABLE): "1,4,2,1,4",
        }  # 260.0

        responses = cls._dummy_table_scaling | cls._dummy_table_response
        patched_connection.return_value = DummyConnection(responses)
        cls._mb = ManagementBase("dummy.co.jp", port=80)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_compute_scaler_voltage(self):
        # V_PU lo must be shifted by 16 (divided by 2^16) and then added to V_PU hi
        v_scaled = self._mb._compute_scaler(RegisterMap.VOLTAGE_SCALING)
        self.assertEqual(180.0, v_scaled)

    def test_compute_scaler_current(self):
        # V_PU lo must be shifted by 16 (divided by 2^16) and then added to V_PU hi
        i_scaled = self._mb._compute_scaler(RegisterMap.CURRENT_SCALING)
        self.assertEqual(80.0, i_scaled)

    def test_get_scaled_value_V(self):
        modbus_register = RegisterMap.BATTERY_VOLTAGE

        val = self._mb.get_scaled_value(
            address=modbus_register.address,
            scale_factor=modbus_register.scale_factor,
            register=modbus_register.registers,
        )

        self.assertEqual(round(24.78515625, 2), val)

    def test_get_scaled_value_A(self):
        modbus_register = RegisterMap.CHARGING_CURRENT

        val = self._mb.get_scaled_value(
            address=modbus_register.address,
            scale_factor=modbus_register.scale_factor,
            register=modbus_register.registers,
        )

        self.assertEqual(round(-0.21484375, 2), val)

    def test_get_scaled_value_W(self):
        modbus_register = RegisterMap.OUTPUT_POWER

        val = self._mb.get_scaled_value(
            address=modbus_register.address,
            scale_factor=modbus_register.scale_factor,
            register=modbus_register.registers,
        )

        self.assertEqual(0.0, val)

    def test_get_scaled_value_Ah(self):
        modbus_register = RegisterMap.AH_CHARGE_RESETABLE

        val = self._mb.get_scaled_value(
            address=modbus_register.address,
            scale_factor=modbus_register.scale_factor,
            register=modbus_register.registers,
        )

        self.assertEqual(19034.2, val)

    def test_get_scaled_value_kWh(self):
        modbus_register = RegisterMap.KWH_CHARGE_RESETABLE

        val = self._mb.get_scaled_value(
            address=modbus_register.address,
            scale_factor=modbus_register.scale_factor,
            register=modbus_register.registers,
        )

        self.assertEqual(260.0, val)


if __name__ == "__main__":
    unittest.main()
