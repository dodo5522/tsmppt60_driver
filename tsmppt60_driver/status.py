#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
TS-MPPT-60 driver's internal modules inherites base modules.
"""

from tsmppt60_driver.base import ChargeControllerStatus


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
            (38, "V", "Battery Voltage", 1),
            (51, "V", "Target Voltage", 1),
            (39, "A", "Charge Current", 1)]

        if not is_limit:
            params.append((58, "W", "Output Power", 1))

        return params


class SolarArrayStatus(ChargeControllerStatus):
    """
    Class to get data about solar array.
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
            (27, "V", "Array Voltage", 1),
            (29, "A", "Array Current", 1)]

        if not is_limit:
            params.extend([
                (61, "V", "Sweep Vmp", 1),
                (62, "V", "Sweep Voc", 1),
                (60, "W", "Sweep Pmax", 1)])

        return params


class TemperaturesStatus(ChargeControllerStatus):
    """
    Class to get data about temperatures sensors.
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
            (35, "C", "Heat Sink Temperature", 1)]

        if not is_limit:
            params.append(
                (37, "C", "Battery Temperature", 1))

        return params


class CountersStatus(ChargeControllerStatus):
    """
    Class to get data about resettable counters.
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
            (52, "Ah", "Amp Hours", 2),
            (56, "kWh", "Kilowatt Hours", 1))

if __name__ == "__main__":
    import doctest
    from minimock import mock

    dummy_charge_controller_status = mock("ChargeControllerStatus")
    doctest.testmod(verbose=True, extraglobs={
        "bat": BatteryStatus(None),
        "array": SolarArrayStatus(None),
        "temp": TemperaturesStatus(None),
        "count": CountersStatus(None)})
