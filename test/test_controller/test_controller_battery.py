from unittest.mock import call

import pytest
from tsmppt60_driver.controller import Battery
from tsmppt60_driver.hal import RegisterMap


def test_get_group(mocked_mod_bus):
    mocked_mod_bus("battery", [])
    assert Battery("", 80).group == "Battery"


def test_get_labels(mocked_mod_bus):
    mocked_mod_bus("battery", [])
    assert Battery("", 80).labels == {
        "Battery Voltage",
        "Target Voltage",
        "Charge Current",
        "Output Power",
        "Battery Temperature",
    }


def test_get_battery_status_all(mocked_mod_bus):
    mocked = mocked_mod_bus(
        "battery",
        [
            12.1,  # battery voltage
            14.2,  # target regulation voltage
            10.3,  # charging current
            98.4,  # output power
            20.5,  # battery temperature
        ],
    )
    assert Battery("", 80).get() == {
        "Battery": {
            "Battery Voltage": {"unit": "V", "value": 12.1},
            "Target Voltage": {"unit": "V", "value": 14.2},
            "Charge Current": {"unit": "A", "value": 10.3},
            "Output Power": {"unit": "W", "value": 98.4},
            "Battery Temperature": {"unit": "C", "value": 20.5},
        }
    }

    assert mocked.get_scaled_value.call_args_list == [
        call(
            RegisterMap.BATTERY_VOLTAGE.address,
            RegisterMap.BATTERY_VOLTAGE.scale_factor,
            RegisterMap.BATTERY_VOLTAGE.registers,
        ),
        call(
            RegisterMap.TARGET_REGULATION_VOLTAGE.address,
            RegisterMap.TARGET_REGULATION_VOLTAGE.scale_factor,
            RegisterMap.TARGET_REGULATION_VOLTAGE.registers,
        ),
        call(
            RegisterMap.CHARGING_CURRENT.address,
            RegisterMap.CHARGING_CURRENT.scale_factor,
            RegisterMap.CHARGING_CURRENT.registers,
        ),
        call(
            RegisterMap.OUTPUT_POWER.address,
            RegisterMap.OUTPUT_POWER.scale_factor,
            RegisterMap.OUTPUT_POWER.registers,
        ),
        call(
            RegisterMap.BATTERY_TEMP.address,
            RegisterMap.BATTERY_TEMP.scale_factor,
            RegisterMap.BATTERY_TEMP.registers,
        ),
    ]


@pytest.mark.parametrize(
    "target_label, register, value",
    [
        ("Battery Voltage", RegisterMap.BATTERY_VOLTAGE, 12.1),
        ("Target Voltage", RegisterMap.TARGET_REGULATION_VOLTAGE, 14.2),
        ("Charge Current", RegisterMap.CHARGING_CURRENT, 10.3),
        ("Output Power", RegisterMap.OUTPUT_POWER, 98.4),
        ("Battery Temperature", RegisterMap.BATTERY_TEMP, 20.5),
    ],
)
def test_get_battery_status_limited(mocked_mod_bus, target_label, register, value):
    mocked = mocked_mod_bus("battery", [value])
    assert Battery("", 80).get(target_labels=[target_label]) == {
        "Battery": {target_label: {"unit": register.scale_factor, "value": value}}
    }

    mocked.get_scaled_value.assert_called_once_with(register.address, register.scale_factor, register.registers)
