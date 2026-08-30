import pytest
from pytest_mock import MockerFixture
from tsmppt60_driver.hal import ModBus


@pytest.fixture
def mocked_mod_bus(mocker: MockerFixture):
    def __mock(target: str, return_values: list[float]):
        mocked = mocker.MagicMock(spec=ModBus)
        mocked.get_scaled_value = mocker.Mock(side_effect=return_values)
        mocker.patch(f"tsmppt60_driver.controller.{target}.ModBus", return_value=mocked)
        return mocked

    return __mock
