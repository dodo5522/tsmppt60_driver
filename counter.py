#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
TS-MPPT-60 resettable counters data library.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from .base import ChargeControllerStatus


class CountersStatus(ChargeControllerStatus):
    """ Class to get data about resettable counters.
    """

    def __init__(self, mb):
        """
        Keyword arguments:
            mb: instance of ManagementBase class
        """
        ChargeControllerStatus.__init__(self, mb, "Resettable Counters")

    def get_params(self):
        """ Get a list of all params for resettable counters.
        """
        return (
            (52, "Ah", "Amp Hours", 2),
            (56, "kWh", "Kilowatt Hours", 1))
