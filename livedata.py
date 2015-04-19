#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
TS-MPPT-60 library to get all status data.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from .base import ManagementBase
from .status import BatteryStatus
from .status import SolarArrayStatus
from .status import TemperaturesStatus
from .status import CountersStatus


class LiveData(object):
    """ Class to get all live data of TS-MPPT-60.
    """

    def __init__(self, host):
        self._mb = ManagementBase(host)

        self._data_objects = {
            obj._group: obj for obj in (
                BatteryStatus(self._mb),
                SolarArrayStatus(self._mb),
                TemperaturesStatus(self._mb),
                CountersStatus(self._mb))}
