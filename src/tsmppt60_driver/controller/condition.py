from ..controller.base import ChargeControllerStatus
from ..hal import Register, RegisterMap


class OperatingConditions(ChargeControllerStatus):
    """
    Class to get data about controller's operating conditions.

    * LED state
    * Charge state
    """

    def __init__(self, mb):
        """
        Initialize OperatingConditions class object.

        Keyword arguments:
        mb -- instance of ManagementBase class
        """
        ChargeControllerStatus.__init__(self, mb, "Condition")

    def _get_params(self, is_limited=True) -> list[Register]:
        """Get and return a list of all params to get the conditions. The param is consisted by (address, scale_factor, label, register).

        Keyword arguments:
        is_limit -- limit the number of getting status

        >>> condition._get_params() == (
        ...     Register(address=49, scale_factor="Numbers", label="LED State", registers=1),
        ...     Register(address=50, scale_factor="Numbers", label="Charge State", registers=1),
        ... )
        True
        >>> condition._get_params(True) == (
        ...     Register(address=49, scale_factor="Numbers", label="LED State", registers=1),
        ...     Register(address=50, scale_factor="Numbers", label="Charge State", registers=1),
        ... )
        True
        >>> condition._get_params(False) == (
        ...     Register(address=49, scale_factor="Numbers", label="LED State", registers=1),
        ...     Register(address=50, scale_factor="Numbers", label="Charge State", registers=1),
        ... )
        True
        """
        return [RegisterMap.LED_STATE, RegisterMap.CHARGE_STATE]


if __name__ == "__main__":
    import doctest

    doctest.testmod(
        verbose=True,
        extraglobs={
            "condition": OperatingConditions(None),
            "Register": Register,
        },
    )
