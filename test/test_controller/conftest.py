import pytest
from pytest_mock import MockerFixture
from tsmppt60_driver import ModBus
from tsmppt60_driver.controller import BatteryStatus, CountersStatus, SolarArrayStatus, TemperaturesStatus


@pytest.fixture
def mocked_controller(mocker: MockerFixture, expected_query_param):
    """Create controller status objects with the ModBus scaler requests mocked."""

    table_scaling = {
        expected_query_param(0x0000, 2): "1,4,4,0,180,0,0",  # VOLTAGE_SCALING
        expected_query_param(0x0002, 2): "1,4,4,0,80,0,0",  # CURRENT_SCALING
    }

    def get_scaling(query_params: list[str]) -> str:
        return table_scaling["&".join(query_params)]

    mocked_get = mocker.patch("tsmppt60_driver.hal.mod_bus.ModBusBase._get", side_effect=get_scaling)

    mb = ModBus("dummy.uribou.mydns.jp", port=80)
    controllers = {
        "battery": BatteryStatus(mb),
        "solar_array": SolarArrayStatus(mb),
        "temperature": TemperaturesStatus(mb),
        "counters": CountersStatus(mb),
    }

    return controllers, mocked_get
