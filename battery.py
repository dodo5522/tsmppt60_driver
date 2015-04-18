#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
TS-MPPT-60 battery data library.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
