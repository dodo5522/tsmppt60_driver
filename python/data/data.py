#!/usr/bin/env python3
# -*- coding:utf-8 -*-

""" This is interface module for human readable data of TS-MPPT-60. """

from .mb import ManagementBase

__author__ = "Takashi Ando"
__copyright__ = "Copyright 2015, My own project"
__credits__ = ["My wife"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Takashi Ando"
__email__ = "noreply@temp.com"
__status__ = "Production"


class ScaledValue(object):
    """ class to manage human readable data got from TS-MPPT-60.
    """

    def __init__(self, mb, group):
        """ calculate the value got from TS-MPPT-60.

        Keyword arguments:
            mb: instance of ManagementBase class
            group: string to indicate the group name
        """
        self._mb = mb
        self._group = group

    def __repr__(self):
        return self._group

    def __str__(self):
        return self._group

    def _get_scaled_value(self, address, scale_factor, register):
        """ calculate the value got from TS-MPPT-60.

        Keyword arguments:
            address: address to get a value
            scale_factor: unit string
            register: register to get a value

        Returns: value as string
        """
        raw_value_str = self._mb.read_modbus(
            address=address, register=register)

        if register > 1:
            values = raw_value_str.split("#")
            raw_value = (int(values[0]) * 65536) + int(values[1])
        else:
            raw_value = int(raw_value_str)
            # raw_value <<= 16
            # raw_value >>= 16
            raw_value &= 0xffff

        if scale_factor == "V":
            return "{0:.2f}".format(
                ((raw_value * self._mb.vscale) / 32768.0 / 10.0))
        elif scale_factor == "A":
            return "{0:.1f}".format(
                (raw_value * self._mb.iscale) / 32768.0 / 10.0)
        elif scale_factor == "W":
            wscale = self._mb.iscale * self._mb.vscale
            return "{0:.0f}".format(
                (raw_value * wscale) / 131072.0 / 100.0)
        elif scale_factor == "Ah":
            return "{0:.1f}".format(raw_value * 0.1)
        elif scale_factor == "kWh":
            return "{0:.0f}".format(raw_value)
        else:
            return "{0:.2f}".format(raw_value)

    def get_value(self, address, scale_factor, label, register):
        """ get the scaled value against the specified address.

        Keyword arguments:
            address: address to get a value
            scale_factor: unit string
            label: label string of got value
            register: register to get a value

        Returns: list of label as str, value as float, unit as str
                 like ("Battery Voltage", 12.1, "V")
        """
        ret_values = []
        ret_values.append(label)
        ret_values.append(
            self._get_scaled_value(address, scale_factor, register))
        ret_values.append(scale_factor)

        return ret_values

    def get_all_value(self):
        """ get all value of a group.

        Returns: tuple of all got values and parameter.
        """
        return [self.get_value(*param) for param in self.get_params()]

    def get_params(self):
        """ get list of all params.
        """
        raise NotImplementedError


class BatteryData(ScaledValue):
    """ class to manage battery data.
    """

    def __init__(self, mb):
        """
        Keyword arguments:
            mb: instance of ManagementBase class
        """
        ScaledValue.__init__(self, mb, "Battery")

    def get_params(self):
        """ get list of all params for battery.
        """
        return (
            (38, "V", "Battery Voltage", 1),
            (51, "V", "Target Voltage", 1),
            (39, "A", "Charge Current", 1),
            (58, "W", "Output Power", 1))


class SolarArrayData(ScaledValue):
    """ class to manage solar array data.
    """

    def __init__(self, mb):
        """
        Keyword arguments:
            mb: instance of ManagementBase class
        """
        ScaledValue.__init__(self, mb, "Array")

    def get_params(self):
        """ get list of all params for solar array.
        """
        return (
            (27, "V", "Array Voltage", 1),
            (29, "A", "Array Current", 1),
            (61, "V", "Sweep Vmp", 1),
            (62, "V", "Sweep Voc", 1),
            (60, "W", "Sweep Pmax", 1))


class TemperaturesData(ScaledValue):
    """ class to manage temperatures data.
    """

    def __init__(self, mb):
        """
        Keyword arguments:
            mb: instance of ManagementBase class
        """
        ScaledValue.__init__(self, mb, "Temperatures")

    def get_params(self):
        """ get list of all params for temperature.
        """
        return ()


class ResettableCountersData(ScaledValue):
    """ class to manage resettable counters data.
    """

    def __init__(self, mb):
        """
        Keyword arguments:
            mb: instance of ManagementBase class
        """
        ScaledValue.__init__(self, mb, "Resettable Counters")

    def get_params(self):
        """ get list of all params for resettable counters.
        """
        return (
            (52, "Ah", "Amp Hours", 2),
            (56, "kWh", "Kilowatt Hours", 1))


class LiveData(object):
    """ class to manage all live data of TS-MPPT-60.
    """

    def __init__(self):
        self._mb = ManagementBase()

        self._data_objects = {
            obj._group: obj for obj in (
                BatteryData(self._mb),
                SolarArrayData(self._mb),
                TemperaturesData(self._mb),
                ResettableCountersData(self._mb))}
