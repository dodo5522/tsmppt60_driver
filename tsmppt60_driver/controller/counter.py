from tsmppt60_driver.controller.base import ChargeControllerStatus
from tsmppt60_driver.hal import Register, RegisterMap


class CountersStatus(ChargeControllerStatus):
    """
    Class to get data about resettable counters.

    * amp hours
    * kilowatt hours
    """

    def __init__(self, mb):
        """
        Initialize CountersStaus class object.

        Keyword arguments:
        mb -- instance of ManagementBase class
        """
        ChargeControllerStatus.__init__(self, mb, "Counter")

    def get_params(self, is_limit=True) -> list[Register]:
        """Get and return a list of all params to get the counters. The param is consisted by (address, scale_factor, label, register).

        Keyword arguments:
        is_limit -- limit the number of getting status

        >>> count.get_params() == (
        ...     Register(address=52, scale_factor="Ah", label="Amp Hours", registers=2),
        ...     Register(address=56, scale_factor="kWh", label="Kilowatt Hours", registers=1),
        ... )
        True
        >>> count.get_params(True) == (
        ...     Register(address=52, scale_factor="Ah", label="Amp Hours", registers=2),
        ...     Register(address=56, scale_factor="kWh", label="Kilowatt Hours", registers=1),
        ... )
        True
        >>> count.get_params(False) == (
        ...     Register(address=52, scale_factor="Ah", label="Amp Hours", registers=2),
        ...     Register(address=56, scale_factor="kWh", label="Kilowatt Hours", registers=1),
        ... )
        True
        """
        return (RegisterMap.AH_CHARGE_RESETABLE, RegisterMap.KWH_CHARGE_RESETABLE)


if __name__ == "__main__":
    import doctest

    from tsmppt60_driver.hal import Register

    doctest.testmod(
        verbose=True,
        extraglobs={
            "count": CountersStatus(None),
            "Register": Register,
        },
    )
