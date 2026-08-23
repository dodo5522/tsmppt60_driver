import unittest
from unittest.mock import patch

from tsmppt60_driver.controller import BatteryStatus, CountersStatus, SolarArrayStatus, TemperaturesStatus
from tsmppt60_driver.hal import ModBus, RegisterMap


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
    """Test case for ChargeControllerStatus."""

    @classmethod
    def _gen_url_parm(cls, addr, reg):
        return "ID=1&F=4&AHI={}&ALO={}&RHI={}&RLO={}".format(addr >> 8, addr & 255, reg >> 8, reg & 255)

    @classmethod
    @patch("tsmppt60_driver.ModBus._get")
    def setUpClass(cls, patched_get):
        def _requests_get(query_params: list[str]) -> str:
            table_scaling = {
                cls._gen_url_parm(0x0000, 2): "1,4,4,0,180,0,0",  # VOLTAGE_SCALING
                cls._gen_url_parm(0x0002, 2): "1,4,4,0,80,0,0",  # CURRENT_SCALING
                cls._gen_url_parm(0x0000, 1): "1,4,2,0,180",  # VOLTAGE_SCALING_HIGH
                cls._gen_url_parm(0x0001, 1): "1,4,2,0,0",  # VOLTAGE_SCALING_LOW
                cls._gen_url_parm(0x0002, 1): "1,4,2,0,80",  # CURRENT_SCALING_HIGH
                cls._gen_url_parm(0x0003, 1): "1,4,2,0,0",
            }  # CURRENT_SCALING_LOW
            return table_scaling["&".join(query_params)]

        patched_get.side_effect = _requests_get

        mb = ModBus("dummy.uribou.mydns.jp", port=80)
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

    @patch("tsmppt60_driver.ModBus._get")
    def test_get_battery_voltage(self, patched_get):
        modbus_register = RegisterMap.BATTERY_VOLTAGE

        def _requests_get(query_params: list[str]) -> str:
            mb_url_parm = "&".join(query_params)
            self.assertEqual(self._gen_url_parm(modbus_register.address, modbus_register.registers), mb_url_parm)
            return "1,4,2,17,160"  # 24.78515625

        patched_get.side_effect = _requests_get

        expected_value = {"group": "Battery", "label": "Battery Voltage", "value": round(24.78515625, 2), "unit": "V"}

        value = self._bat.get_status(
            modbus_register.address,
            modbus_register.scale_factor,
            modbus_register.label,
            modbus_register.registers,
        )

        self.assertEqual(set(expected_value.items()), set(value.items()))

    @patch("tsmppt60_driver.ModBus._get")
    def test_get_target_voltage(self, patched_get):
        modbus_register = RegisterMap.TARGET_REGULATION_VOLTAGE

        def _requests_get(query_params: list[str]) -> str:
            mb_url_parm = "&".join(query_params)
            self.assertEqual(mb_url_parm, self._gen_url_parm(modbus_register.address, modbus_register.registers))
            return "1,4,2,0,0"  # 0.0

        patched_get.side_effect = _requests_get

        expected_value = {"group": "Battery", "label": "Target Voltage", "value": 0.0, "unit": "V"}

        value = self._bat.get_status(
            modbus_register.address,
            modbus_register.scale_factor,
            modbus_register.label,
            modbus_register.registers,
        )

        self.assertEqual(set(expected_value.items()), set(value.items()))

    @patch("tsmppt60_driver.ModBus._get")
    def test_get_output_power(self, patched_get):
        patched_get.return_value = "1,4,2,0,0"  # 0.0

    @patch("tsmppt60_driver.ModBus._get")
    def test_get_battery_temperature(self, patched_get):
        patched_get.return_value = "1,4,2,0,25"  # 25.0


if __name__ == "__main__":
    unittest.main(verbosity=2)
