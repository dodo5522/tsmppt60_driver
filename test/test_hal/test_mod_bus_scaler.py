import pytest
from pytest import param
from tsmppt60_driver.hal import RegisterMap


@pytest.mark.parametrize(
    "response, expected",
    [
        param("1,4,4,0,180,0,0", 180.0, id="no fractional part"),
        param("1,4,4,0,180,128,0", 180.5, id="with fractional part"),
    ],
)
def test_get_voltage_scaler(mocked_mod_bus_scaler, response, expected, expected_query_param):
    md, connection = mocked_mod_bus_scaler(200, response)
    actual = md.get_voltage_scaler()
    assert actual == expected

    request_args = connection.request.call_args.args
    assert request_args[0] == "GET"
    assert (
        request_args[1]
        == f"/MBCSV.cgi?{expected_query_param(RegisterMap.VOLTAGE_SCALING.address, RegisterMap.VOLTAGE_SCALING.registers)}"
    )


@pytest.mark.parametrize(
    "response, expected",
    [
        param("1,4,4,0,80,0,0", 80.0, id="no fractional part"),
        param("1,4,4,0,80,64,0", 80.25, id="with fractional part"),
    ],
)
def test_get_current_scaler(mocked_mod_bus_scaler, response, expected, expected_query_param):
    md, connection = mocked_mod_bus_scaler(200, response)
    actual = md.get_current_scaler()
    assert actual == expected

    request_args = connection.request.call_args.args
    assert request_args[0] == "GET"
    assert (
        request_args[1]
        == f"/MBCSV.cgi?{expected_query_param(RegisterMap.CURRENT_SCALING.address, RegisterMap.CURRENT_SCALING.registers)}"
    )
