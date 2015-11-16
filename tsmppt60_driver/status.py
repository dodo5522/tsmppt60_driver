#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
TS-MPPT-60 driver's modules inherites base modules.
"""

from .base import ChargeControllerStatus


class BatteryStatus(ChargeControllerStatus):
    """
    Class to get data about charging battery.
    """

    def __init__(self, mb, is_limit=True):
        """
        Initialize BatteryStatus class object.

        :param mb: instance of ManagementBase class
        :param is_limit: limit the number of getting status
        """
        ChargeControllerStatus.__init__(self, mb, "Battery")
        self._is_limit = is_limit

    def get_params(self):
        """
        Get a list of all params for battery charging status.

        :return: Parameter list to get battery status.
        """
        params = [
            (38, "V", "Battery Voltage", 1),
            (51, "V", "Target Voltage", 1),
            (39, "A", "Charge Current", 1)]

        if not self._is_limit:
            params.append((58, "W", "Output Power", 1))

        return params


class SolarArrayStatus(ChargeControllerStatus):
    """
    Class to get data about solar array.
    """

    def __init__(self, mb, is_limit=True):
        """
        Initialize SolarArrayStatus class object.

        :param mb: instance of ManagementBase class
        :param is_limit: limit the number of getting status
        """
        ChargeControllerStatus.__init__(self, mb, "Array")
        self._is_limit = is_limit

    def get_params(self):
        """
        Get a list of all params for solar array status.

        :return: Parameter list to get solar array status.
        """
        params = [
            (27, "V", "Array Voltage", 1),
            (29, "A", "Array Current", 1)]

        if not self._is_limit:
            params.extend([
                (61, "V", "Sweep Vmp", 1),
                (62, "V", "Sweep Voc", 1),
                (60, "W", "Sweep Pmax", 1)])

        return params


class TemperaturesStatus(ChargeControllerStatus):
    """
    Class to get data about temperatures sensors.
    """

    def __init__(self, mb, is_limit=True):
        """
        Initialize SolarArrayStatus class object.

        :param mb: instance of ManagementBase class
        :param is_limit: limit the number of getting status
        """
        ChargeControllerStatus.__init__(self, mb, "Temperature")
        self._is_limit = is_limit

    def get_params(self):
        """
        Get a list of all params for temperature sensors.

        :return: Parameter list to get temperature status.
        """
        params = [
            (35, "C", "Heat Sink Temperature", 1)]

        if not self._is_limit:
            params.append(
                (37, "C", "Battery Temperature", 1))

        return params


class CountersStatus(ChargeControllerStatus):
    """
    Class to get data about resettable counters.
    """

    def __init__(self, mb, is_limit=True):
        """
        Initialize CountersStaus class object.

        :param mb: instance of ManagementBase class
        :param is_limit: limit the number of getting status
        """
        ChargeControllerStatus.__init__(self, mb, "Counter")
        self._is_limit = is_limit

    def get_params(self):
        """
        Get a list of all params for resettable counters.

        :return: Parameter list to get counter status.
        """
        return (
            (52, "Ah", "Amp Hours", 2),
            (56, "kWh", "Kilowatt Hours", 1))
