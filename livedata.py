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
        self._status_dict = {
            obj.get_group(): obj for obj in (
                BatteryStatus(self._mb),
                SolarArrayStatus(self._mb),
                TemperaturesStatus(self._mb),
                CountersStatus(self._mb))}
        self._status_list = (group for group in self._status_dict.keys())

    def __len__(self):
        return len(self._status_dict)

    def __getitem__(self, key):
        return self._status_dict[key]

    def __iter__(self):
        self._status_list_index = 0
        return self._status_list

    def __next__(self):
        self._status_list_index += 1

        if self._status_list_index >= len(self._status_list):
            raise StopIteration

        return self._status_list[self._status_list_index]
