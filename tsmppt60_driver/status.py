#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""TS-MPPT-60 driver's internal modules inherites base modules."""

import logging

from tsmppt60_driver.base import ModbusRegisterTable


class ChargeControllerStatus(object):
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
        handler.setFormatter(logging.Formatter(
            "%(asctime)s %(name)s %(levelname)s: %(message)s",
            "%Y/%m/%d %p %l:%M:%S"))

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
        ret_values["value"] = self._mb.get_scaled_value(
            address, scale_factor, register)
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
        return [self.get_status(*param) for param in self.get_params(is_limit)]

    def get_params(self, is_limit=True):
        """Get and return a list of all params of the inherited class's group.

        Keyword arguments:
        is_limit -- limit the number of getting status
            ((61, "V", "Sweep Vmp", 1),
             (62, "V", "Sweep Voc", 1),
             (60, "W", "Sweep Pmax", 1))
        """
        raise NotImplementedError


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

    def get_params(self, is_limit=True):
        """Get and return a list of all params to get the battery status. The param is consisted by (address, scale_factor, label, register).

        Keyword arguments:
        is_limit -- limit the number of getting status

        >>> bat.get_params() == [
        ...     (38, 'V', 'Battery Voltage', 1),
        ...     (51, 'V', 'Target Voltage', 1),
        ...     (39, 'A', 'Charge Current', 1)]
        True
        >>> bat.get_params(True) == [
        ...     (38, 'V', 'Battery Voltage', 1),
        ...     (51, 'V', 'Target Voltage', 1),
        ...     (39, 'A', 'Charge Current', 1)]
        True
        >>> bat.get_params(False) == [
        ...     (38, 'V', 'Battery Voltage', 1),
        ...     (51, 'V', 'Target Voltage', 1),
        ...     (39, 'A', 'Charge Current', 1),
        ...     (58, 'W', 'Output Power', 1)]
        True
        """
        params = [
            ModbusRegisterTable.BATTERY_VOLTAGE,
            ModbusRegisterTable.TARGET_REGULATION_VOLTAGE,
            ModbusRegisterTable.CHARGING_CURRENT]

        if not is_limit:
            params.append(ModbusRegisterTable.OUTPUT_POWER)

        return params


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

    def get_params(self, is_limit=True):
        """Get and return a list of all params to get the solar array status. The param is consisted by (address, scale_factor, label, register).

        Keyword arguments:
        is_limit -- limit the number of getting status

        >>> array.get_params() == [
        ...    (27, 'V', 'Array Voltage', 1),
        ...    (29, 'A', 'Array Current', 1)]
        True
        >>> array.get_params(True) == [
        ...    (27, 'V', 'Array Voltage', 1),
        ...    (29, 'A', 'Array Current', 1)]
        True
        >>> array.get_params(False) == [
        ...    (27, 'V', 'Array Voltage', 1),
        ...    (29, 'A', 'Array Current', 1),
        ...    (61, "V", "Sweep Vmp", 1),
        ...    (62, "V", "Sweep Voc", 1),
        ...    (60, "W", "Sweep Pmax", 1)]
        True
        """
        params = [
            ModbusRegisterTable.ARRAY_VOLTAGE,
            ModbusRegisterTable.ARRAY_CURRENT]

        if not is_limit:
            params.extend([
                ModbusRegisterTable.VMP_LAST_SWEEP,
                ModbusRegisterTable.VOC_LAST_SWEEP,
                ModbusRegisterTable.POWER_LAST_SWEEP])

        return params


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

    def get_params(self, is_limit=True):
        """Get and return a list of all params to get the temperatures. The param is consisted by (address, scale_factor, label, register).

        Keyword arguments:
        is_limit -- limit the number of getting status

        >>> temp.get_params() == [
        ...    (35, 'C', 'Heat Sink Temperature', 1)]
        True
        >>> temp.get_params(True) == [
        ...    (35, 'C', 'Heat Sink Temperature', 1)]
        True
        >>> temp.get_params(False) == [
        ...    (35, 'C', 'Heat Sink Temperature', 1),
        ...    (37, 'C', 'Battery Temperature', 1)]
        True
        """
        params = [
            ModbusRegisterTable.HEATSINK_TEMP]

        if not is_limit:
            params.append(
                ModbusRegisterTable.BATTERY_TEMP)

        return params


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

    def get_params(self, is_limit=True):
        """Get and return a list of all params to get the counters. The param is consisted by (address, scale_factor, label, register).

        Keyword arguments:
        is_limit -- limit the number of getting status

        >>> count.get_params() == (
        ...    (52, 'Ah', 'Amp Hours', 2),
        ...    (56, 'kWh', 'Kilowatt Hours', 1))
        True
        >>> count.get_params(True) == (
        ...    (52, 'Ah', 'Amp Hours', 2),
        ...    (56, 'kWh', 'Kilowatt Hours', 1))
        True
        >>> count.get_params(False) == (
        ...    (52, 'Ah', 'Amp Hours', 2),
        ...    (56, 'kWh', 'Kilowatt Hours', 1))
        True
        """
        return (
            ModbusRegisterTable.AH_CHARGE_RESETABLE,
            ModbusRegisterTable.KWH_CHARGE_RESETABLE)


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

    def get_params(self, is_limit=True):
        """Get and return a list of all params to get the conditions. The param is consisted by (address, scale_factor, label, register).

        Keyword arguments:
        is_limit -- limit the number of getting status

        >>> condition.get_params() == (
        ...    (49, '', 'LED State', 1),
        ...    (50, '', 'Charge State', 1))
        True
        >>> condition.get_params(True) == (
        ...    (49, '', 'LED State', 1),
        ...    (50, '', 'Charge State', 1))
        True
        >>> condition.get_params(False) == (
        ...    (49, '', 'LED State', 1),
        ...    (50, '', 'Charge State', 1))
        True
        """
        return (
            ModbusRegisterTable.LED_STATE,
            ModbusRegisterTable.CHARGE_STATE)


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True, extraglobs={
        "bat": BatteryStatus(None),
        "array": SolarArrayStatus(None),
        "temp": TemperaturesStatus(None),
        "count": CountersStatus(None),
        "condition": OperatingConditions(None)})
