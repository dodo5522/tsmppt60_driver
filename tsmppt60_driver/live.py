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


class SystemStatus(object):
    """ This is iterator object containing the system status of TS-MPPT-60.
        Use this object like below.

        status_all = StatusAll("192.168.1.20")

        for stat in status_all:
            # This stat has some group and you can get it by str().
            group = str(stat)
            # get_all_status method returns all data of the stat.
            live_data = stat.get_status_all()
            # live_data is tuple. first item is id like "Battery Voltage"
            print("id: {}".format(live_data[0]))
            # second item is value like "12.4"
            print("val: {}".format(live_data[1]))
            # third item is unit like "V"
            print("unit: {}".format(live_data[2]))
    """

    def __init__(self, host):
        _mb = ManagementBase(host)

        self._status = (
            BatteryStatus(_mb),
            SolarArrayStatus(_mb),
            TemperaturesStatus(_mb),
            CountersStatus(_mb))

    def __len__(self):
        return len(self._status)

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index >= len(self._status):
            raise StopIteration

        stat_obj = self._status[self._index]
        self._index += 1

        return stat_obj
