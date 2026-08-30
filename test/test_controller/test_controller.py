import pytest

from tsmppt60_driver.hal import RegisterMap


@pytest.mark.parametrize(
    "controller, modbus_register, response, expected",
    [
        pytest.param(
            "battery",
            RegisterMap.BATTERY_VOLTAGE,
            "1,4,2,17,160",
            {"group": "Battery", "label": "Battery Voltage", "value": 24.79, "unit": "V"},
            id="battery-voltage",
        ),
        pytest.param(
            "battery",
            RegisterMap.TARGET_REGULATION_VOLTAGE,
            "1,4,2,0,0",
            {"group": "Battery", "label": "Target Voltage", "value": 0.0, "unit": "V"},
            id="target-voltage",
        ),
        pytest.param(
            "battery",
            RegisterMap.OUTPUT_POWER,
            "1,4,2,0,0",
            {"group": "Battery", "label": "Output Power", "value": 0.0, "unit": "W"},
            id="output-power",
        ),
        pytest.param(
            "temperature",
            RegisterMap.BATTERY_TEMP,
            "1,4,2,0,25",
            {"group": "Temperature", "label": "Battery Temperature", "value": 25.0, "unit": "C"},
            id="battery-temperature",
        ),
    ],
)
def test_get_status(mocked_controller, controller, modbus_register, response, expected):
    controllers, mocked_get = mocked_controller

    def get_status(query_params: list[str]) -> str:
        assert "&".join(query_params) == (
            f"ID=1&F=4&AHI={modbus_register.address >> 8}&ALO={modbus_register.address & 255}"
            f"&RHI={modbus_register.registers >> 8}&RLO={modbus_register.registers & 255}"
        )
        return response

    mocked_get.reset_mock()
    mocked_get.side_effect = get_status

    actual = controllers[controller].get_status(
        modbus_register.address,
        modbus_register.scale_factor,
        modbus_register.label,
        modbus_register.registers,
    )

    assert actual == expected
