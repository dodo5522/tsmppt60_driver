import pytest
from pytest import param


@pytest.mark.parametrize(
    "registers, response, expected",
    [
        param(1, "1,4,2,17,160", 4512, id="single register with positive raw from 2 values"),
        param(2, "1,4,4,17,160,10,1", 295700993, id="double registers with positive raw from 4 values"),
        param(1, "1,4,2,255,168", -88, id="single register with negative raw from 2 values"),
        param(
            2,
            "1,4,4,255,168,10,1",
            4289202689,
            # e.g. hourmeter / alarm bitfield / Ah charge
            id="double registers preserve unsigned value with high bit set",
        ),
    ],
)
def test_get_value(mocked_mod_bus, registers: int, response, expected, expected_query_param):
    md, connection = mocked_mod_bus(200, response, 0.0, 0.0)
    actual = md.get_value(address=0, register=registers)
    assert actual == expected

    request_args = connection.request.call_args.args
    assert request_args[0] == "GET"
    assert request_args[1] == f"/MBCSV.cgi?{expected_query_param(0, registers)}"


def test_get_value_error(mocked_mod_bus, expected_query_param):
    md, connection = mocked_mod_bus(200, "1,4,4,17,160,10,1", 0.0, 0.0)

    with pytest.raises(ValueError) as e:
        md.get_value(address=0, register=1)

    assert isinstance(e.value, ValueError)
    assert e.value.args[0] == "Requested registers=1 unmatched to the number of register values=[4512, 2561]"

    request_args = connection.request.call_args.args
    assert request_args[0] == "GET"
    assert request_args[1] == f"/MBCSV.cgi?{expected_query_param(0, 1)}"


@pytest.mark.parametrize(
    "registers, scale_factor, response, expected",
    [
        param(1, "V", "1,4,2,17,160", 24.78515625, id="voltage"),
        param(1, "A", "1,4,2,255,168", -0.21484375, id="current"),
        param(1, "W", "1,4,2,0,23", 2.53, id="Watt power"),
        param(2, "Ah", "1,4,4,0,2,231,134", 19034.2, id="ampere hour"),
        param(1, "C", "1,4,2,0,25", 25.0, id="degree Celsius"),
        param(1, "kWh", "1,4,2,1,4", 260.0, id="kilo watt hour"),
    ],
)
def test_get_scaled_value(
    mocked_mod_bus, registers: int, scale_factor: str, response: str, expected: float, expected_query_param
):
    md, connection = mocked_mod_bus(200, response, 180.0, 80.0)
    actual = md.get_scaled_value(
        address=0,
        scale_factor=scale_factor,
        register=registers,
    )
    assert round(actual, 2) == round(expected, 2)

    request_args = connection.request.call_args.args
    assert request_args[0] == "GET"
    assert request_args[1] == f"/MBCSV.cgi?{expected_query_param(0, registers)}"
