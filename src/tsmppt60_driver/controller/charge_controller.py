from ..controller.base import ControllerBase
from ..hal import ModBus, RegisterMap


class ChargeController(ControllerBase):
    """Controller for charge-controller operating conditions.

    The controller exposes LED state, charge state, heat-sink temperature,
    resettable amp hours, and resettable kilowatt hours.
    """

    def __init__(self, host: str, port: int, *, debug: bool = False):
        """
        Initialize a ChargeController controller.

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
                RegisterMap.LED_STATE,
                RegisterMap.CHARGE_STATE,
                RegisterMap.HEATSINK_TEMP,
                RegisterMap.AH_CHARGE_RESETABLE,
                RegisterMap.KWH_CHARGE_RESETABLE,
            ],
            debug=debug,
        )
