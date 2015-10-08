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


class LiveStatus(object):
    """ This is iterator object containing all live status data of TS-MPPT-60.
        Use this object like below.

        live = LiveStatus("192.168.1.20")

        for stat in live:
            # This stat has some group and you can get it by str().
            group = str(stat)
            # get_all_status method returns all data of the stat.
            live_data = stat.get_all_status()
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
        return self._status

    def __next__(self):
        self._index += 1

        if self._index >= len(self._status):
            raise StopIteration

        return self._status[self._index]
