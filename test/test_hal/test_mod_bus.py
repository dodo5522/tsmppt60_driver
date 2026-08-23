import pytest
from pytest import param

from tsmppt60_driver.hal.mod_bus import RegisterMap


@pytest.mark.parametrize(
    "register, response, expected",
    [
        param(RegisterMap.BATTERY_VOLTAGE, "1,4,2,17,160", 24.78515625, id="BATTERY_VOLTAGE"),
        param(RegisterMap.CHARGING_CURRENT, "1,4,2,255,168", -0.21484375, id="CHARGING_CURRENT"),
        param(RegisterMap.TARGET_REGULATION_VOLTAGE, "1,4,2,0,0", 0.0, id="TARGET_REGULATION_VOLTAGE"),
        param(RegisterMap.OUTPUT_POWER, "1,4,2,0,0", 0.0, id="OUTPUT_POWER"),
        param(RegisterMap.ARRAY_VOLTAGE, "1,4,2,0,84", 0.46, id="ARRAY_VOLTAGE"),
        param(RegisterMap.ARRAY_CURRENT, "1,4,2,0,0", 0.0, id="ARRAY_CURRENT"),
        param(RegisterMap.VMP_LAST_SWEEP, "1,4,2,11,208", 16.61, id="VMP_LAST_SWEEP"),
        param(RegisterMap.VOC_LAST_SWEEP, "1,4,2,15,193", 22.15, id="VOC_LAST_SWEEP"),
        param(RegisterMap.POWER_LAST_SWEEP, "1,4,2,0,23", 2.53, id="POWER_LAST_SWEEP"),
        param(RegisterMap.HEATSINK_TEMP, "1,4,2,0,7", 7.0, id="HEATSINK_TEMP"),
        param(RegisterMap.BATTERY_TEMP, "1,4,2,0,25", 25.0, id="BATTERY_TEMP"),
        param(RegisterMap.AH_CHARGE_RESETABLE, "1,4,4,0,2,231,134", 19034.2, id="AH_CHARGE_RESETABLE"),
        param(RegisterMap.KWH_CHARGE_RESETABLE, "1,4,2,1,4", 260.0, id="KWH_CHARGE_RESETABLE"),
    ],
)
def test_get_scaled_value(mocked_mod_bus, register, response, expected):
    md, _ = mocked_mod_bus(200, response, 180.0, 80.0)
    actual = md.get_scaled_value(
        address=register.address,
        scale_factor=register.scale_factor,
        register=register.registers,
    )
    assert round(actual, 2) == round(expected, 2)
