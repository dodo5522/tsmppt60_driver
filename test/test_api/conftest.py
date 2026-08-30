import pytest
from pytest_mock import MockerFixture


@pytest.fixture
def mocked_controllers(mocker: MockerFixture):
    """Mock controller classes used by SystemStatus."""

    controller_names = ("Battery", "SolarArray", "ChargeController")
    constructors = {}
    controllers = {}

    for name in controller_names:
        controller = mocker.MagicMock(name=f"mock_{name}")
        controller.group = name
        controller.get.return_value = {name: {f"{name} label": {"value": 1.0, "unit": ""}}}

        constructors[name] = mocker.patch(
            f"tsmppt60_driver.api.status.{name}",
            return_value=controller,
        )
        controllers[name] = controller

    return constructors, controllers
