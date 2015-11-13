#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
TS-MPPT-60 status data library.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from .base import ChargeControllerStatus


class BatteryStatus(ChargeControllerStatus):
    """ Class to get data about charging battery.
    """

    def __init__(self, mb):
        """
        Keyword arguments:
            mb: instance of ManagementBase class
        """
        ChargeControllerStatus.__init__(self, mb, "Battery")

    def get_params(self):
        """ Get a list of all params for battery charging status.
        """
        return (
            (38, "V", "Battery Voltage", 1),
            (51, "V", "Target Voltage", 1),
            (39, "A", "Charge Current", 1),
            (58, "W", "Output Power", 1))


class SolarArrayStatus(ChargeControllerStatus):
    """ Class to get data about solar array.
    """

    def __init__(self, mb):
        """
        Keyword arguments:
            mb: instance of ManagementBase class
        """
        ChargeControllerStatus.__init__(self, mb, "Array")

    def get_params(self):
        """ Get a list of all params for solar array status.
        """
        return (
            (27, "V", "Array Voltage", 1),
            (29, "A", "Array Current", 1),
            (61, "V", "Sweep Vmp", 1),
            (62, "V", "Sweep Voc", 1),
            (60, "W", "Sweep Pmax", 1))


class TemperaturesStatus(ChargeControllerStatus):
    """ Class to get data about temperatures sensors.
    """

    def __init__(self, mb):
        """
        Keyword arguments:
            mb: instance of ManagementBase class
        """
        ChargeControllerStatus.__init__(self, mb, "Temperature")

    def get_params(self):
        """ Get a list of all params for temperature sensors.
        """
        return (
            (37, "C", "Battery Temperature", 1),
            (35, "C", "Heat Sink Temperature", 1))


class CountersStatus(ChargeControllerStatus):
    """ Class to get data about resettable counters.
    """

    def __init__(self, mb):
        """
        Keyword arguments:
            mb: instance of ManagementBase class
        """
        ChargeControllerStatus.__init__(self, mb, "Counter")

    def get_params(self):
        """ Get a list of all params for resettable counters.
        """
        return (
            (52, "Ah", "Amp Hours", 2),
            (56, "kWh", "Kilowatt Hours", 1))
