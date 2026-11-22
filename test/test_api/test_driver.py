from datetime import datetime, timezone

import time_machine

from tsmppt60_driver.api import TsMppt60


def test_init_creates_controllers_with_connection_parameters(mocked_controllers):
    constructors, _ = mocked_controllers

    TsMppt60("dummy.example.com", port=8080, debug=True)

    for constructor in constructors.values():
        constructor.assert_called_once_with("dummy.example.com", 8080, debug=True)


def test_groups_returns_available_controller_groups(mocked_controllers):
    system_status = TsMppt60("dummy.example.com")

    assert system_status.groups == {"Battery", "SolarArray", "ChargeController"}


@time_machine.travel(datetime(1985, 10, 26, 1, 24, tzinfo=timezone.utc))
def test_get_returns_status_from_all_groups(mocked_controllers):
    _, controllers = mocked_controllers
    system_status = TsMppt60("dummy.example.com")

    assert system_status.get() == {
        "Battery": {"Battery label": {"value": 1.0, "unit": ""}},
        "SolarArray": {"SolarArray label": {"value": 1.0, "unit": ""}},
        "ChargeController": {"ChargeController label": {"value": 1.0, "unit": ""}},
        "measured_at": "1985-10-26T01:24:00+00:00",
    }

    for controller in controllers.values():
        controller.get.assert_called_once_with()


@time_machine.travel(datetime(1985, 10, 26, 1, 24, tzinfo=timezone.utc))
def test_get_returns_status_only_from_selected_groups(mocked_controllers):
    _, controllers = mocked_controllers
    system_status = TsMppt60("dummy.example.com")

    assert system_status.get(groups={"Battery", "ChargeController"}) == {
        "Battery": {"Battery label": {"value": 1.0, "unit": ""}},
        "ChargeController": {"ChargeController label": {"value": 1.0, "unit": ""}},
        "measured_at": "1985-10-26T01:24:00+00:00",
    }

    controllers["Battery"].get.assert_called_once_with()
    controllers["ChargeController"].get.assert_called_once_with()
    controllers["SolarArray"].get.assert_not_called()
