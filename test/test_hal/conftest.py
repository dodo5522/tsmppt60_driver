import pytest
from pytest_mock import MockerFixture
from tsmppt60_driver import ModBus, ModBusScaler


@pytest.fixture
def expected_query_param():
    return lambda address, registers: "ID=1&F=4&AHI={}&ALO={}&RHI={}&RLO={}".format(
        address >> 8,
        address & 255,
        registers >> 8,
        registers & 255,
    )


@pytest.fixture
def mocked_mod_bus(mocker: MockerFixture):
    def __mod_bus(response_status: int, response_text: str, voltage_scaler: float, current_scaler: float):
        response = mocker.MagicMock()
        response.status = response_status
        response.read = mocker.Mock(return_value=response_text.encode("ASCII"))

        connection = mocker.MagicMock()
        connection.request = mocker.Mock()
        connection.getresponse = mocker.Mock(return_value=response)

        mocker.patch("tsmppt60_driver.hal.base.mod_bus.HTTPConnection", return_value=connection)
        mocker.patch("tsmppt60_driver.hal.mod_bus.ModBusScaler.get_voltage_scaler", return_value=voltage_scaler)
        mocker.patch("tsmppt60_driver.hal.mod_bus.ModBusScaler.get_current_scaler", return_value=current_scaler)

        return ModBus("dummy.co.jp", port=80), connection

    return __mod_bus


@pytest.fixture
def mocked_mod_bus_scaler(mocker: MockerFixture):
    def __mod_bus_scaler(response_status: int, response_text: str):
        response = mocker.MagicMock()
        response.status = response_status
        response.read = mocker.Mock(return_value=response_text.encode("ASCII"))

        connection = mocker.MagicMock()
        connection.request = mocker.Mock()
        connection.getresponse = mocker.Mock(return_value=response)

        mocker.patch("tsmppt60_driver.hal.base.mod_bus.HTTPConnection", return_value=connection)
        return ModBusScaler("dummy.co.jp", port=80), connection

    return __mod_bus_scaler
