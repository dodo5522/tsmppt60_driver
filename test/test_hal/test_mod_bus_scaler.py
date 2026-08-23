import pytest
from pytest import param


@pytest.mark.parametrize(
    "response, expected",
    [
        param("1,4,4,0,180,0,0", 180.0, id="no fractional part"),
        param("1,4,4,0,180,128,0", 180.5, id="with fractional part"),
    ],
)
def test_get_voltage_scaler(mocked_mod_bus_scaler, response, expected):
    md, connection = mocked_mod_bus_scaler(200, response)
    actual = md.get_voltage_scaler()
    assert actual == expected

    request_args = connection.request.call_args.args
    assert request_args[0] == "GET"
    assert request_args[1] == "/MBCSV.cgi?ID=1&F=4&AHI=0&ALO=0&RHI=0&RLO=2"


@pytest.mark.parametrize(
    "response, expected",
    [
        param("1,4,4,0,80,0,0", 80.0, id="no fractional part"),
        param("1,4,4,0,80,64,0", 80.25, id="with fractional part"),
    ],
)
def test_get_current_scaler(mocked_mod_bus_scaler, response, expected):
    md, connection = mocked_mod_bus_scaler(200, response)
    actual = md.get_current_scaler()
    assert actual == expected

    request_args = connection.request.call_args.args
    assert request_args[0] == "GET"
    assert request_args[1] == "/MBCSV.cgi?ID=1&F=4&AHI=0&ALO=2&RHI=0&RLO=2"
