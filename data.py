#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
TS-MPPT-60 data structure library.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from .mb import ManagementBase


class Data(object):
    """ Super class to get data about charging status.
    """

    def __init__(self, mb, group):
        """
        Keyword arguments:
            mb: instance of ManagementBase class.
            group: string to indicate this instance name.
        """
        self._mb = mb
        self._group = group

    def __repr__(self):
        return '<%s [%s]>'.format(type(self).__name__, self._group)

    def __str__(self):
        return '<%s [%s]>'.format(type(self).__name__, self._group)

    def _get_scaled_value(self, address, scale_factor, register):
        """ Calculate a status value got from TS-MPPT-60.

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
            if raw_value & 0x8000:
                raw_value ^= 0xffff
                raw_value = -1 * (raw_value + 1)

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

    def get(self, address, scale_factor, label, register):
        """ Get a data against the specified address, register, etc.

        Keyword arguments:
            address: address to get a value
            scale_factor: unit string
            label: label string of got value
            register: register to get a value

        Returns: list of label as str, value as float, unit as str
                 like ("Battery Voltage", "12.1", "V")
        """
        ret_values = []
        ret_values.append(label)
        ret_values.append(
            self._get_scaled_value(address, scale_factor, register))
        ret_values.append(scale_factor)

        return ret_values

    def get_all(self):
        """ Get all data against the inherited class's paramter list.

        Returns: tuple of all got values and parameter.
        """
        return [self.get(*param) for param in self.get_params()]

    def get_params(self):
        """ Get list of all params of the inherited class's group.
        """
        raise NotImplementedError


class BatteryData(Data):
    """ Class to get data about charging battery.
    """

    def __init__(self, mb):
        """
        Keyword arguments:
            mb: instance of ManagementBase class
        """
        Data.__init__(self, mb, "Battery")

    def get_params(self):
        """ Get a list of all params for battery charging status.
        """
        return (
            (38, "V", "Battery Voltage", 1),
            (51, "V", "Target Voltage", 1),
            (39, "A", "Charge Current", 1),
            (58, "W", "Output Power", 1))


class SolarArrayData(Data):
    """ Class to get data about solar array.
    """

    def __init__(self, mb):
        """
        Keyword arguments:
            mb: instance of ManagementBase class
        """
        Data.__init__(self, mb, "Array")

    def get_params(self):
        """ Get a list of all params for solar array status.
        """
        return (
            (27, "V", "Array Voltage", 1),
            (29, "A", "Array Current", 1),
            (61, "V", "Sweep Vmp", 1),
            (62, "V", "Sweep Voc", 1),
            (60, "W", "Sweep Pmax", 1))


class TemperaturesData(Data):
    """ Class to get data about temperatures sensors.
    """

    def __init__(self, mb):
        """
        Keyword arguments:
            mb: instance of ManagementBase class
        """
        Data.__init__(self, mb, "Temperatures")

    def get_params(self):
        """ Get a list of all params for temperature sensors.
        """
        return ()


class ResettableCountersData(Data):
    """ Class to get data about resettable counters.
    """

    def __init__(self, mb):
        """
        Keyword arguments:
            mb: instance of ManagementBase class
        """
        Data.__init__(self, mb, "Resettable Counters")

    def get_params(self):
        """ Get a list of all params for resettable counters.
        """
        return (
            (52, "Ah", "Amp Hours", 2),
            (56, "kWh", "Kilowatt Hours", 1))


class LiveData(object):
    """ Class to get all live data of TS-MPPT-60.
    """

    def __init__(self, host):
        self._mb = ManagementBase(host)

        self._data_objects = {
            obj._group: obj for obj in (
                BatteryData(self._mb),
                SolarArrayData(self._mb),
                TemperaturesData(self._mb),
                ResettableCountersData(self._mb))}
