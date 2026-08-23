import logging
from abc import ABC, abstractmethod

from tsmppt60_driver.hal import Register


class ChargeControllerStatus(ABC):
    """Abstract class to get data about charge controller status."""

    def __init__(self, mb, group, debug=False):
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

    def get_status(self, address, scale_factor, label, register):
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

    def get_status_all(self, is_limit=True):
        """
        Get and return all data against the inherited class's paramter list.

            { "group": "Battery",
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

        Keyword arguments:
        is_limit -- limit the number of getting status
        """
        return [self.get_status(p.address, p.scale_factor, p.label, p.registers) for p in self.get_params(is_limit)]

    @abstractmethod
    def get_params(self, is_limit=True) -> list[Register]:
        """Get and return a list of all params of the inherited class's group.

        Keyword arguments:
        is_limit -- limit the number of getting status
            ((61, "V", "Sweep Vmp", 1),
             (62, "V", "Sweep Voc", 1),
             (60, "W", "Sweep Pmax", 1))
        """
        raise NotImplementedError()
