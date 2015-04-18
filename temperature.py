#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
TS-MPPT-60 temperatures data library.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from .base import ChargeControllerStatus


class TemperaturesStatus(ChargeControllerStatus):
    """ Class to get data about temperatures sensors.
    """

    def __init__(self, mb):
        """
        Keyword arguments:
            mb: instance of ManagementBase class
        """
        ChargeControllerStatus.__init__(self, mb, "Temperatures")

    def get_params(self):
        """ Get a list of all params for temperature sensors.
        """
        return ()
