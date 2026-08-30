from ..hal import ModBus, RegisterMap
from ._base import ControllerBase


class Battery(ControllerBase):
    """Controller for battery-related status data.

    The controller exposes battery voltage, target voltage, charging current,
    output power, and battery temperature.
    """

    def __init__(self, host: str, port: int, *, debug: bool = False):
        """Initialize a Battery controller.

        Args:
            host: TS-MPPT-60 host address like "192.168.1.20"
            port: TS-MPPT-60 port number like 80
            debug: Enable debug logging when ``True``.
        """
        ControllerBase.__init__(
            self,
            ModBus(host, port=port),
            self.__class__.__name__,
            [
                RegisterMap.BATTERY_VOLTAGE,
                RegisterMap.TARGET_REGULATION_VOLTAGE,
                RegisterMap.CHARGING_CURRENT,
                RegisterMap.OUTPUT_POWER,
                RegisterMap.BATTERY_TEMP,
            ],
            debug=debug,
        )
