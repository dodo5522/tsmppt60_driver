from ..controller import (
    Battery,
    ChargeController,
    ControllerBase,
    SolarArray,
)


class SystemStatus:
    """Read status data from the TS-MPPT-60 controller groups.

    By default, :meth:`get` returns all groups in a nested dictionary. Pass
    a set of group names to ``groups`` to limit the result, for example:

        SystemStatus("192.168.1.20").get(groups={"Battery"})

    The available groups can be obtained from the :attr:`groups` property.
    """

    def __init__(self, host, *, port: int = 80, debug: bool = False):
        """Initialize a SystemStatus instance.

        Args:
            host: Host address of the TS-MPPT-60 live view, such as
                ``"192.168.1.20"``.
            port: Port number of the live view.
            debug: Enable debug logging when ``True``.
        """
        battery = Battery(host, port, debug=debug)
        array = SolarArray(host, port, debug=debug)
        charge = ChargeController(host, port, debug=debug)

        self._controllers: dict[str, ControllerBase] = {
            battery.group: battery,
            array.group: array,
            charge.group: charge,
        }

    @property
    def groups(self) -> set[str]:
        """Return the names of the available controller groups."""
        return set(self._controllers.keys())

    def get(self, *, groups: set[str] | None = None):
        """Return status data for the selected controller groups.

        If ``groups`` is omitted, status data from all available groups is
        returned. The result is keyed by group name, with each group mapping
        labels to values and units.

        Args:
            groups: Names of the controller groups to include. Available
                names can be obtained from :attr:`groups`.

        Returns:
            A nested dictionary containing the selected status data.
        """
        target_groups = groups if groups else self.groups
        status = {}

        for target_group in target_groups:
            if controller := self._controllers.get(target_group):
                status.update(controller.get())

        return status
