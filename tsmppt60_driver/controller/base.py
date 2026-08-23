import logging
from abc import ABC, abstractmethod

from tsmppt60_driver.hal import ModBus, Register


class ChargeControllerStatus(ABC):
    """Abstract class to get data about charge controller status."""

    def __init__(self, mb: ModBus, group: str, debug: bool = False):
        """Initialize class object.

        Keyword arguments:
        mb -- instance of ManagementBase class.
        group -- string to indicate this instance name.
        debug -- If True, logging is enabled.
        """
        self._mb = mb
        self._group = group

        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s", "%Y/%m/%d %p %l:%M:%S")
        )

        self._logger = logging.getLogger(type(self).__name__)
        self._logger.addHandler(handler)

        if debug:
            self._logger.setLevel(logging.DEBUG)

    def __repr__(self):
        return self._group

    def __str__(self):
        return self._group

    def get_status(self, address: int, scale_factor: str, label: str, register: int):
        """
        Get and return a data against the specified address, register, etc. like below.

            {
                "group": "battery",
                "label": "Battery Voltage",
                "value": 12.1,
                "unit": "V"
            }

        Keyword arguments:
        address -- address to get a value
        scale_factor -- unit string
        label -- label string of got value
        register -- register to get a value
        """
        ret_values = {}
        ret_values["group"] = self._group
        ret_values["label"] = label
        ret_values["value"] = self._mb.get_scaled_value(address, scale_factor, register)
        ret_values["unit"] = scale_factor

        return ret_values

    def get_status_all(self, is_limited: bool = True):
        """
        Get and return all data against the inherited class's parameter list.

            {
                "group": "Battery",
                "label": "Battery Voltage",
                "value": 12.1,
                "unit": "V"
            },
            {
                "group": "Battery",
                "label": "Charge Current",
                "value": 8.4,
                "unit": "A"
            }

        Keyword Args:
            is_limited: limit the number of getting status
        """
        return [self.get_status(p.address, p.scale_factor, p.label, p.registers) for p in self._get_params(is_limited)]

    @abstractmethod
    def _get_params(self, is_limited: bool) -> list[Register]:
        """Get and return a list of all params of the inherited class's group.

        Args:
            is_limited: limit the number of getting status
        """
        raise NotImplementedError()
