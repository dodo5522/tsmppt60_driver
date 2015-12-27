#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
TS-MPPT-60 driver's internal modules inherites base modules.
"""

from tsmppt60_driver.base import ChargeControllerStatus
from tsmppt60_driver.base import ModbusRegisterTable


class BatteryStatus(ChargeControllerStatus):
    """
    This class gives the following battery status.

    * battery voltage
    * target voltage
    * charge current
    * output power
    """

    def __init__(self, mb):
        """
        Initialize BatteryStatus class object.

        :param mb: instance of ManagementBase class
        """
        ChargeControllerStatus.__init__(self, mb, "Battery")

    def get_params(self, is_limit=True):
        """
        Get a list of all params to get the battery status.
        The param is consisted by (address, scale_factor, label, register).

        :param is_limit: limit the number of getting status
        :return: Parameter list to get battery status.

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
    """
    Class to get data about solar array.

    * array voltage
    * array current
    * sweep vmp
    * sweep voc
    * sweep pmax
    """

    def __init__(self, mb):
        """
        Initialize SolarArrayStatus class object.

        :param mb: instance of ManagementBase class
        """
        ChargeControllerStatus.__init__(self, mb, "Array")

    def get_params(self, is_limit=True):
        """
        Get a list of all params to get the solar array status.
        The param is consisted by (address, scale_factor, label, register).

        :param is_limit: limit the number of getting status
        :return: Parameter list to get solar array status.

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
    """
    Class to get data about temperatures sensors.

    * heat sink temperature
    * battery temperature
    """

    def __init__(self, mb):
        """
        Initialize SolarArrayStatus class object.

        :param mb: instance of ManagementBase class
        """
        ChargeControllerStatus.__init__(self, mb, "Temperature")

    def get_params(self, is_limit=True):
        """
        Get a list of all params to get the temperatures.
        The param is consisted by (address, scale_factor, label, register).

        :param is_limit: limit the number of getting status
        :return: Parameter list to get temperature status.

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

        :param mb: instance of ManagementBase class
        """
        ChargeControllerStatus.__init__(self, mb, "Counter")

    def get_params(self, is_limit=True):
        """
        Get a list of all params to get the counters.
        The param is consisted by (address, scale_factor, label, register).

        :param is_limit: limit the number of getting status
        :return: Parameter list to get counter status.

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

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True, extraglobs={
        "bat": BatteryStatus(None),
        "array": SolarArrayStatus(None),
        "temp": TemperaturesStatus(None),
        "count": CountersStatus(None)})
