#!/usr/bin/env python3
# -*- coding:utf-8 -*-

""" This is low level module to manage TS-MPPT-60. """

import requests
import logging

__author__ = "Takashi Ando"
__copyright__ = "Copyright 2015, My own project"
__credits__ = ["My wife"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Takashi Ando"
__email__ = "noreply@temp.com"
__status__ = "Production"


class ManagementBase(object):
    """ class to manage raw data got from TS-MPPT-60.
    """
    _MBID = 0x01
    _MBP = 502

    _V_SCALE_LDEC = 0
    _V_SCALE_RDEC = 1
    _I_SCALE_LDEC = 2
    _I_SCALE_RDEC = 3

    def __init__(self, url="http://192.168.1.20", cgi="MBCSV.cgi", debug=True):
        """ Initialization

        Keyword arguments:
            url: URL of TS-MPPT-60 live view
            cgi: CGI file name to get the information
            debug: If True, logging is enabled.

        Returns:
            None
        """
        self._url = url + "/" + cgi

        def _get_scale(ldec, rdec):
            L = self.read_modbus(self._MBID, ldec, 1)
            R = self.read_modbus(self._MBID, rdec, 1)
            return int(L) + (int(R) / 65535)

        self.vscale = _get_scale(self._V_SCALE_LDEC, self._V_SCALE_RDEC)
        self.iscale = _get_scale(self._I_SCALE_LDEC, self._I_SCALE_RDEC)

        if debug:
            logging.basicConfig(level=logging.DEBUG)

    def _get(self, mbid, addr, reg, field=4):
        """ Get the value against the MBID, Address, Register, and Field.

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
        logging.debug("{0}".format(res.request.url))

        return res.text

    def read_modbus(self, mbid=_MBID, address=0, register=0):
        """ Get the value against the MBID, Address, and Register.

        Keyword arguments:
            mbid: MBID
            addr: Address to get information
            reg: Register to get information

        Returns: String like ...
        """
        raw_value_str = self._get(mbid, address, register)
        raw_values = [int(v) for v in raw_value_str.split(",")]
        idx_max = raw_values[2]
        idx_value = 3
        ret_str = ""

        logging.debug(raw_value_str)

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
