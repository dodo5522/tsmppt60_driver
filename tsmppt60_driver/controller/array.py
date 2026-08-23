from tsmppt60_driver.controller.base import ChargeControllerStatus
from tsmppt60_driver.hal import Register, RegisterMap


class SolarArrayStatus(ChargeControllerStatus):
    """Class to get data about solar array.

    * array voltage
    * array current
    * sweep vmp
    * sweep voc
    * sweep pmax
    """

    def __init__(self, mb):
        """Initialize SolarArrayStatus class object.

        Keyword arguments:
        mb -- instance of ManagementBase class
        """
        ChargeControllerStatus.__init__(self, mb, "Array")

    def get_params(self, is_limit=True) -> list[Register]:
        """Get and return a list of all params to get the solar array status. The param is consisted by (address, scale_factor, label, register).

        Keyword arguments:
        is_limit -- limit the number of getting status

        >>> array.get_params() == [
        ...     Register(address=27, scale_factor="V", label="Array Voltage", registers=1),
        ...     Register(address=29, scale_factor="A", label="Array Current", registers=1),
        ... ]
        True
        >>> array.get_params(True) == [
        ...     Register(address=27, scale_factor="V", label="Array Voltage", registers=1),
        ...     Register(address=29, scale_factor="A", label="Array Current", registers=1),
        ... ]
        True
        >>> array.get_params(False) == [
        ...     Register(address=27, scale_factor="V", label="Array Voltage", registers=1),
        ...     Register(address=29, scale_factor="A", label="Array Current", registers=1),
        ...     Register(address=61, scale_factor="V", label="Sweep Vmp", registers=1),
        ...     Register(address=62, scale_factor="V", label="Sweep Voc", registers=1),
        ...     Register(address=60, scale_factor="W", label="Sweep Pmax", registers=1),
        ... ]
        True
        """
        params = [RegisterMap.ARRAY_VOLTAGE, RegisterMap.ARRAY_CURRENT]

        if not is_limit:
            params.extend(
                [
                    RegisterMap.VMP_LAST_SWEEP,
                    RegisterMap.VOC_LAST_SWEEP,
                    RegisterMap.POWER_LAST_SWEEP,
                ]
            )

        return params


if __name__ == "__main__":
    import doctest

    doctest.testmod(
        verbose=True,
        extraglobs={
            "array": SolarArrayStatus(None),
            "Register": Register,
        },
    )
