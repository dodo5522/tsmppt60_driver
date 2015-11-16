#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
TS-MPPT-60 driver's base modules.
"""

import requests
import logging


class Logger(object):
    _FORMAT_LOG_MSG = "%(asctime)s %(name)s %(levelname)s: %(message)s"
    _FORMAT_LOG_DATE = "%Y/%m/%d %p %l:%M:%S"

    def __init__(self, log_file_path=None, debug=False):
        """
        Initialize Logger class object.

        :param log_file_path: Path to record log file.
        :param debug: If True, logging is enabled.
        """
        self.logger = logging.getLogger(type(self).__name__)

        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            fmt=self._FORMAT_LOG_MSG, datefmt=self._FORMAT_LOG_DATE)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        if log_file_path:
            handler = logging.FileHandler(log_file_path, mode="a")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        if debug:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)


class ManagementBase(object):
    """
    Class to get raw data from TS-MPPT-60.
    """
    _MBID = 0x01
    _MBP = 502

    _V_SCALE_LDEC = 0
    _V_SCALE_RDEC = 1
    _I_SCALE_LDEC = 2
    _I_SCALE_RDEC = 3

    def __init__(self, host, cgi="MBCSV.cgi", debug=False):
        """
        Initialize class object.

        :param host: Host address like "192.168.1.20" of TS-MPPT-60 live view
        :param cgi: CGI file name to get the information
        :param debug: If True, logging is enabled.
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
        """
        Get raw data against MBID, Address, Register, and Field.

        :param mbid: MBID
        :param addr: Address to get information
        :param reg: Register to get information
        :param field: Field to get information
        :return: String like "1,4,1,1,1"
        """
        params = []
        params.append("ID=" + str(mbid))
        params.append("F=" + str(field))
        params.append("AHI=" + str(addr >> 8))
        params.append("ALO=" + str(addr & 255))
        params.append("RHI=" + str(reg >> 8))
        params.append("RLO=" + str(reg & 255))

        res = requests.get(
            "{0}?{1}".format(self._url, "&".join(params)), timeout=(5, 15))
        self._logger.debug("{0}".format(res.request.url))

        return res.text

    def read_modbus(self, mbid=_MBID, address=0, register=0):
        """
        Read the value against MBID, Address, and Register.

        :param mbid: MBID
        :param addr: Address to get information
        :param reg: Register to get information
        :return: String with short integer (ex. 16bit value).
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
    """
    Abstract class to get data about charge controller status.
    """

    def __init__(self, mb, group, debug=False):
        """
        Initialize class object.

        :param mb: instance of ManagementBase class.
        :param group: string to indicate this instance name.
        :param debug: If True, logging is enabled.
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

    def _get_scaled_value(self, address, scale_factor, register):
        """
        Calculate a status value got from TS-MPPT-60.

        :param address: address to get a value
        :param scale_factor: unit string
        :param register: register to get a value
        :return: value as string
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

    def get_status(self, address, scale_factor, label, register):
        """
        Get a data against the specified address, register, etc.

        :param address: address to get a value
        :param scale_factor: unit string
        :param label: label string of got value
        :param register: register to get a value
        :return: str of group, label as str, value as float, unit as str like
            {
                "group": "battery",
                "label": "Battery Voltage",
                "value": 12.1,
                "unit": "V"
            }
        """
        ret_values = {}
        ret_values["group"] = self._group
        ret_values["label"] = label
        ret_values["value"] = float(self._get_scaled_value(
            address, scale_factor, register))
        ret_values["unit"] = scale_factor

        return ret_values

    def get_status_all(self):
        """
        Get all data against the inherited class's paramter list.

        :return: tuple of all got values and parameter like this.
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
        """
        return [self.get_status(*param) for param in self.get_params()]

    def get_params(self):
        """
        Get list of all params of the inherited class's group.

        :return: tuple of parameter list like this.
            ((61, "V", "Sweep Vmp", 1),
             (62, "V", "Sweep Voc", 1),
             (60, "W", "Sweep Pmax", 1))
        """
        raise NotImplementedError
