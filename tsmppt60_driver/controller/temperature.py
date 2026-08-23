from tsmppt60_driver.controller.base import ChargeControllerStatus
from tsmppt60_driver.hal import Register, RegisterMap


class TemperaturesStatus(ChargeControllerStatus):
    """Class to get data about temperatures sensors.

    * heat sink temperature
    * battery temperature
    """

    def __init__(self, mb):
        """Initialize SolarArrayStatus class object.

        Keyword arguments:
        mb -- instance of ManagementBase class
        """
        ChargeControllerStatus.__init__(self, mb, "Temperature")

    def _get_params(self, is_limited=True) -> list[Register]:
        """Get and return a list of all params to get the temperatures. The param is consisted by (address, scale_factor, label, register).

        Keyword arguments:
        is_limit -- limit the number of getting status

        >>> temp._get_params() == [
        ...     Register(address=35, scale_factor="C", label="Heat Sink Temperature", registers=1),
        ... ]
        True
        >>> temp._get_params(True) == [
        ...     Register(address=35, scale_factor="C", label="Heat Sink Temperature", registers=1),
        ... ]
        True
        >>> temp._get_params(False) == [
        ...     Register(address=35, scale_factor="C", label="Heat Sink Temperature", registers=1),
        ...     Register(address=37, scale_factor="C", label="Battery Temperature", registers=1),
        ... ]
        True
        """
        params = [RegisterMap.HEATSINK_TEMP]

        if not is_limited:
            params.append(RegisterMap.BATTERY_TEMP)

        return params


if __name__ == "__main__":
    import doctest

    from tsmppt60_driver.hal import Register

    doctest.testmod(
        verbose=True,
        extraglobs={
            "temp": TemperaturesStatus(None),
            "Register": Register,
        },
    )
