import pytest
from pytest_mock import MockerFixture

from tsmppt60_driver.controller import BatteryStatus, CountersStatus, SolarArrayStatus, TemperaturesStatus
from tsmppt60_driver.hal import ModBus


def _gen_url_param(address: int, registers: int) -> str:
    return "ID=1&F=4&AHI={}&ALO={}&RHI={}&RLO={}".format(
        address >> 8,
        address & 255,
        registers >> 8,
        registers & 255,
    )


@pytest.fixture
def mocked_controller(mocker: MockerFixture):
    """Create controller status objects with the ModBus scaler requests mocked."""

    table_scaling = {
        _gen_url_param(0x0000, 2): "1,4,4,0,180,0,0",  # VOLTAGE_SCALING
        _gen_url_param(0x0002, 2): "1,4,4,0,80,0,0",  # CURRENT_SCALING
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
