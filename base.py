#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
TS-MPPT-60 data structure library.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import requests
import logging


class ManagementBase(object):
    """ Class to get raw data from TS-MPPT-60.
    """
    _MBID = 0x01
    _MBP = 502

    _V_SCALE_LDEC = 0
    _V_SCALE_RDEC = 1
    _I_SCALE_LDEC = 2
    _I_SCALE_RDEC = 3

    def __init__(self, host, cgi="MBCSV.cgi", debug=False):
        """
        Keyword arguments:
            host: Host address like "192.168.1.20" of TS-MPPT-60 live view
            cgi: CGI file name to get the information
            debug: If True, logging is enabled.
        """
        self._logger = logging.getLogger(type(self).__name__)
        self._logger.addHandler(logging.StreamHandler())

        if debug:
            self._logger.setLevel(logging.DEBUG)

        self._url = "http://" + host + "/" + cgi

        def _get_scale(ldec, rdec):
            L = self.read_modbus(self._MBID, ldec, 1)
            R = self.read_modbus(self._MBID, rdec, 1)
            return L + str(int(R) / 65535)

        self.vscale = float(_get_scale(self._V_SCALE_LDEC, self._V_SCALE_RDEC))
        self.iscale = float(_get_scale(self._I_SCALE_LDEC, self._I_SCALE_RDEC))

    def _get(self, mbid, addr, reg, field=4):
        """ Get raw data against MBID, Address, Register, and Field.

        Keyword arguments:
            mbid: MBID
            addr: Address to get information
            reg: Register to get information
            field: Field to get information

        Returns: String like "1,4,1,1,1"
        """
        params = []
        params.append("ID=" + str(mbid))
        params.append("F=" + str(field))
        params.append("AHI=" + str(addr >> 8))
        params.append("ALO=" + str(addr & 255))
        params.append("RHI=" + str(reg >> 8))
        params.append("RLO=" + str(reg & 255))

        res = requests.get("{0}?{1}".format(self._url, "&".join(params)))
        self._logger.debug("{0}".format(res.request.url))

        return res.text

    def read_modbus(self, mbid=_MBID, address=0, register=0):
        """ Read the value against MBID, Address, and Register.

        Keyword arguments:
            mbid: MBID
            addr: Address to get information
            reg: Register to get information

        Returns: String with short integer (ex. 16bit value).
        """
        raw_value_str = self._get(mbid, address, register)
        raw_values = [int(v) for v in raw_value_str.split(",")]
        idx_max = raw_values[2]
        idx_value = 3
        ret_str = ""

        self._logger.debug(raw_value_str)

        while idx_value < idx_max + 2:
            ret_short = (raw_values[idx_value] * 256)
            idx_value += 1
            ret_short += raw_values[idx_value]
            idx_value += 1

            if idx_value < idx_max + 2:
                ret_str += str(ret_short) + "#"
            else:
                ret_str += str(ret_short)

        return ret_str


class ChargeControllerStatus(object):
    """ Abstract class to get data about charge controller status.
    """

    def __init__(self, mb, group, debug=False):
        """
        Keyword arguments:
            mb: instance of ManagementBase class.
            group: string to indicate this instance name.
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
        elif scale_factor == "kWh" or scale_factor == "C":
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
