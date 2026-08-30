from unittest.mock import call

import pytest
from tsmppt60_driver.controller import SolarArray
from tsmppt60_driver.hal import RegisterMap


def test_get_group(mocked_mod_bus):
    mocked_mod_bus("solar_array", [])
    assert SolarArray("", 80).group == "SolarArray"


def test_get_labels(mocked_mod_bus):
    mocked_mod_bus("solar_array", [])
    assert SolarArray("", 80).labels == {
        "Array Voltage",
        "Array Current",
        "Sweep Vmp",
        "Sweep Voc",
        "Sweep Pmax",
    }


def test_get_solar_array_status_all(mocked_mod_bus):
    mocked = mocked_mod_bus(
        "solar_array",
        [
            53.4,  # array voltage
            3.2,  # array current
            53.1,  # sweep Vmp
            60.1,  # sweep Voc
            73.0,  # sweep Pmax
        ],
    )
    assert SolarArray("", 80).get() == {
        "SolarArray": {
            "Array Voltage": {"unit": "V", "value": 53.4},
            "Array Current": {"unit": "A", "value": 3.2},
            "Sweep Vmp": {"unit": "V", "value": 53.1},
            "Sweep Voc": {"unit": "V", "value": 60.1},
            "Sweep Pmax": {"unit": "W", "value": 73.0},
        }
    }

    assert mocked.get_scaled_value.call_args_list == [
        call(
            RegisterMap.ARRAY_VOLTAGE.address,
            RegisterMap.ARRAY_VOLTAGE.scale_factor,
            RegisterMap.ARRAY_VOLTAGE.registers,
        ),
        call(
            RegisterMap.ARRAY_CURRENT.address,
            RegisterMap.ARRAY_CURRENT.scale_factor,
            RegisterMap.ARRAY_CURRENT.registers,
        ),
        call(
            RegisterMap.VMP_LAST_SWEEP.address,
            RegisterMap.VMP_LAST_SWEEP.scale_factor,
            RegisterMap.VMP_LAST_SWEEP.registers,
        ),
        call(
            RegisterMap.VOC_LAST_SWEEP.address,
            RegisterMap.VOC_LAST_SWEEP.scale_factor,
            RegisterMap.VOC_LAST_SWEEP.registers,
        ),
        call(
            RegisterMap.POWER_LAST_SWEEP.address,
            RegisterMap.POWER_LAST_SWEEP.scale_factor,
            RegisterMap.POWER_LAST_SWEEP.registers,
        ),
    ]


@pytest.mark.parametrize(
    "target_label, register, value",
    [
        ("Array Voltage", RegisterMap.ARRAY_VOLTAGE, 53.4),
        ("Array Current", RegisterMap.ARRAY_CURRENT, 3.2),
        ("Sweep Vmp", RegisterMap.VMP_LAST_SWEEP, 53.1),
        ("Sweep Voc", RegisterMap.VOC_LAST_SWEEP, 60.1),
        ("Sweep Pmax", RegisterMap.POWER_LAST_SWEEP, 73.0),
    ],
)
def test_get_solar_array_status_limited(mocked_mod_bus, target_label, register, value):
    mocked = mocked_mod_bus("solar_array", [value])
    assert SolarArray("", 80).get(target_labels=[target_label]) == {
        "SolarArray": {target_label: {"unit": register.scale_factor, "value": value}}
    }

    mocked.get_scaled_value.assert_called_once_with(register.address, register.scale_factor, register.registers)
