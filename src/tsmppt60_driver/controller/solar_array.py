from ..controller.base import ControllerBase
from ..hal import ModBus, RegisterMap


class SolarArray(ControllerBase):
    """Controller for solar-array status data.

    The controller exposes array voltage, array current, and the most recent
    Vmp, Voc, and Pmax sweep values.
    """

    def __init__(self, host: str, port: int, *, debug: bool = False):
        """Initialize a SolarArray controller.

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
                RegisterMap.ARRAY_VOLTAGE,
                RegisterMap.ARRAY_CURRENT,
                RegisterMap.VMP_LAST_SWEEP,
                RegisterMap.VOC_LAST_SWEEP,
                RegisterMap.POWER_LAST_SWEEP,
            ],
            debug=debug,
        )
