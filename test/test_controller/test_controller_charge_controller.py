from unittest.mock import call

import pytest
from tsmppt60_driver.controller import ChargeController
from tsmppt60_driver.hal import RegisterMap


def test_get_group(mocked_mod_bus):
    mocked_mod_bus("charge_controller", [])
    assert ChargeController("", 80).group == "ChargeController"


def test_get_labels(mocked_mod_bus):
    mocked_mod_bus("charge_controller", [])
    assert ChargeController("", 80).labels == {
        "LED State",
        "Charge State",
        "Heat Sink Temperature",
        "Amp Hours",
        "Kilowatt Hours",
    }


def test_get_charge_controller_status_all(mocked_mod_bus):
    mocked = mocked_mod_bus(
        "charge_controller",
        [
            11,  # LED state
            3,  # charge state
            20.5,  # heat sink temperature
            19034.2,  # amp hours
            237.0,  # kilowatt hours
        ],
    )
    assert ChargeController("", 80).get() == {
        "ChargeController": {
            "LED State": {"unit": "Numbers", "value": 11},
            "Charge State": {"unit": "Numbers", "value": 3},
            "Heat Sink Temperature": {"unit": "C", "value": 20.5},
            "Amp Hours": {"unit": "Ah", "value": 19034.2},
            "Kilowatt Hours": {"unit": "kWh", "value": 237.0},
        }
    }

    assert mocked.get_scaled_value.call_args_list == [
        call(
            RegisterMap.LED_STATE.address,
            RegisterMap.LED_STATE.scale_factor,
            RegisterMap.LED_STATE.registers,
        ),
        call(
            RegisterMap.CHARGE_STATE.address,
            RegisterMap.CHARGE_STATE.scale_factor,
            RegisterMap.CHARGE_STATE.registers,
        ),
        call(
            RegisterMap.HEATSINK_TEMP.address,
            RegisterMap.HEATSINK_TEMP.scale_factor,
            RegisterMap.HEATSINK_TEMP.registers,
        ),
        call(
            RegisterMap.AH_CHARGE_RESETABLE.address,
            RegisterMap.AH_CHARGE_RESETABLE.scale_factor,
            RegisterMap.AH_CHARGE_RESETABLE.registers,
        ),
        call(
            RegisterMap.KWH_CHARGE_RESETABLE.address,
            RegisterMap.KWH_CHARGE_RESETABLE.scale_factor,
            RegisterMap.KWH_CHARGE_RESETABLE.registers,
        ),
    ]


@pytest.mark.parametrize(
    "target_label, register, value",
    [
        ("LED State", RegisterMap.LED_STATE, 11),
        ("Charge State", RegisterMap.CHARGE_STATE, 3),
        ("Heat Sink Temperature", RegisterMap.HEATSINK_TEMP, 20.5),
        ("Amp Hours", RegisterMap.AH_CHARGE_RESETABLE, 19034.2),
        ("Kilowatt Hours", RegisterMap.KWH_CHARGE_RESETABLE, 237.0),
    ],
)
def test_get_charge_controller_status_limited(mocked_mod_bus, target_label, register, value):
    mocked = mocked_mod_bus("charge_controller", [value])
    assert ChargeController("", 80).get(target_labels=[target_label]) == {
        "ChargeController": {target_label: {"unit": register.scale_factor, "value": value}}
    }

    mocked.get_scaled_value.assert_called_once_with(register.address, register.scale_factor, register.registers)
