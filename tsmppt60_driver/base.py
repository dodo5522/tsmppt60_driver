#!/usr/bin/env python
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


class ModbusRegisterTable:
    VOLTAGE_SCALING_HIGH      = (0x0000, "", "Voltage Scaling High", 1)
    VOLTAGE_SCALING_LOW       = (0x0001, "", "Voltage Scaling Low", 1)
    CURRENT_SCALING_HIGH      = (0x0002, "", "Current Scaling High", 1)
    CURRENT_SCALING_LOW       = (0x0003, "", "Current Scaling Low", 1)
    SOFTWARE_VERSION          = (0x0004, "", "Software Version", 1)

    BATTERY_VOLTAGE           = (0x0026, "V", "Battery Voltage", 1)
    CHARGING_CURRENT          = (0x0027, "A", "Charge Current", 1)
    TARGET_REGULATION_VOLTAGE = (0x0033, "V", "Target Voltage", 1)
    OUTPUT_POWER              = (0x003a, "W", "Output Power", 1)
    ARRAY_VOLTAGE             = (0x001b, "V", "Array Voltage", 1)
    ARRAY_CURRENT             = (0x001d, "A", "Array Current", 1)
    VMP_LAST_SWEEP            = (0x003d, "V", "Sweep Vmp", 1)
    VOC_LAST_SWEEP            = (0x003e, "V", "Sweep Voc", 1)
    POWER_LAST_SWEEP          = (0x003c, "W", "Sweep Pmax", 1)
    HEATSINK_TEMP             = (0x0023, "C", "Heat Sink Temperature", 1)
    BATTERY_TEMP              = (0x0025, "C", "Battery Temperature", 1)
    AH_CHARGE_RESETABLE       = (0x0034, "Ah", "Amp Hours", 2)
    KWH_CHARGE_RESETABLE      = (0x0038, "kWh", "Kilowatt Hours", 1)


class ManagementBase(object):
    """
    @brief Class to get raw data from TS-MPPT-60.
    @detail MODBUS ID is fixed to 1 as written on data sheet
            TSMPPT.APP_.Modbus.EN_.10.2.pdf.
    """
    _ID_MODBUS = 0x01

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

        self.vscale = float(self.compute_scaler(
            ModbusRegisterTable.VOLTAGE_SCALING_HIGH[0],
            ModbusRegisterTable.VOLTAGE_SCALING_LOW[0]))
        self.iscale = float(self.compute_scaler(
            ModbusRegisterTable.CURRENT_SCALING_HIGH[0],
            ModbusRegisterTable.CURRENT_SCALING_LOW[0]))

    def _get(self, addr, reg, mbid=_ID_MODBUS, field=4):
        """
        Get raw data against MBID, Address, Register, and Field.

        :param addr: Address to get information
        :param reg: Register to get information
        :param mbid: MBID
        :param field: Field to get information
        :return: String like "1,4,1,1,1"

        >>> mb._get(addr=0x0000, reg=1)
        '1,4,2,0,180'
        >>> mb._get(addr=0x0001, reg=1)
        '1,4,2,0,0'
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

    def read_modbus(self, address, register, mbid=_ID_MODBUS):
        """
        Read the value against MBID, Address, and Register.

        :param addr: Address to get information
        :param reg: Register to get information
        :param mbid: MBID
        :return: String with short integer (ex. 16bit value).
        >>> mb.read_modbus(0x0000, 1)
        '180'
        >>> mb.read_modbus(0x0001, 1)
        '0'
        """
        raw_value_str = self._get(address, register, mbid)
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

    def compute_scaler(self, address_high, address_low):
        """
        Compute a voltage/current scaler as written on data sheet page 8 or 25.
        Vscaling = whole.fraction = [V_PU hi].[V_PU lo]

        Example:
        Address:Value(hex):Variable Name
        V_PU HI byte:0x004E = 78
        V_PU LO byte:0x03A6 = 934

        V_PU lo must be shifted by 16 (divided by 2^16)
        and then added to V_PU hi Vscaling = 78 + 934/65536 = 78.01425

        :param address_high: High address like V_PU Hi byte
        :param address_low: Low address like V_PU Hi byte
        :return: float value computed as scaler
        >>> mb.compute_scaler(0, 1)
        180.0
        >>> mb.compute_scaler(2, 3)
        80.0
        """
        L = self.read_modbus(address_high, 1)
        R = self.read_modbus(address_low, 1)
        return float(L) + (int(R) / 65536)


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
        raw_value_str = self._mb.read_modbus(address, register)

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
                raw_value * self._mb.vscale / 32768.0)
        elif scale_factor == "A":
            return "{0:.1f}".format(
                raw_value * self._mb.iscale / 32768.0)
        elif scale_factor == "W":
            wscale = self._mb.iscale * self._mb.vscale
            return "{0:.0f}".format(
                raw_value * wscale / 131072.0)
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

    def get_status_all(self, is_limit=True):
        """
        Get all data against the inherited class's paramter list.

        :param is_limit: limit the number of getting status
        :return: tuple of all got values and parameter like this.
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
        """
        return [self.get_status(*param) for param in self.get_params(is_limit)]

    def get_params(self, is_limit=True):
        """
        Get list of all params of the inherited class's group.

        :param is_limit: limit the number of getting status
        :return: tuple of parameter list like this.
            ((61, "V", "Sweep Vmp", 1),
             (62, "V", "Sweep Voc", 1),
             (60, "W", "Sweep Pmax", 1))
        """
        raise NotImplementedError

if __name__ == "__main__":
    import doctest
    dummy_host = "192.168.1.20"
    doctest.testmod(
            verbose=True,
            extraglobs={"mb": ManagementBase(host=dummy_host)})
