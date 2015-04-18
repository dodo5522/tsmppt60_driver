#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
TS-MPPT-60 solar array data library.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from .base import ChargeControllerStatus


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
