from tsmppt60_driver.controller.base import ChargeControllerStatus
from tsmppt60_driver.hal import Register, RegisterMap


class BatteryStatus(ChargeControllerStatus):
    """
    This class gives the following battery status.

    * battery voltage
    * target voltage
    * charge current
    * output power
    """

    def __init__(self, mb):
        """Initialize BatteryStatus class object.

        Keyword arguments:
        mb -- instance of ManagementBase class
        """
        ChargeControllerStatus.__init__(self, mb, "Battery")

    def get_params(self, is_limit=True) -> list[Register]:
        """Get and return a list of all params to get the battery status. The param is consisted by (address, scale_factor, label, register).

        Keyword arguments:
        is_limit -- limit the number of getting status

        >>> bat.get_params() == [
        ...     Register(address=38, scale_factor="V", label="Battery Voltage", registers=1),
        ...     Register(address=51, scale_factor="V", label="Target Voltage", registers=1),
        ...     Register(address=39, scale_factor="A", label="Charge Current", registers=1),
        ... ]
        True
        >>> bat.get_params(True) == [
        ...     Register(address=38, scale_factor="V", label="Battery Voltage", registers=1),
        ...     Register(address=51, scale_factor="V", label="Target Voltage", registers=1),
        ...     Register(address=39, scale_factor="A", label="Charge Current", registers=1),
        ... ]
        True
        >>> bat.get_params(False) == [
        ...     Register(address=38, scale_factor="V", label="Battery Voltage", registers=1),
        ...     Register(address=51, scale_factor="V", label="Target Voltage", registers=1),
        ...     Register(address=39, scale_factor="A", label="Charge Current", registers=1),
        ...     Register(address=58, scale_factor="W", label="Output Power", registers=1),
        ... ]
        True
        """
        params = [
            RegisterMap.BATTERY_VOLTAGE,
            RegisterMap.TARGET_REGULATION_VOLTAGE,
            RegisterMap.CHARGING_CURRENT,
        ]

        if not is_limit:
            params.append(RegisterMap.OUTPUT_POWER)

        return params


if __name__ == "__main__":
    import doctest

    doctest.testmod(
        verbose=True,
        extraglobs={
            "bat": BatteryStatus(None),
            "Register": Register,
        },
    )
