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
    """ This class is iterator and dict containing all live data of TS-MPPT-60.
        Use this object like below.

        live = LiveData("192.168.1.20")

        for group in live:
            # group is like "Battery" and this is key
            live_data_obj = live[group]
            # get_all_status method returns all data of the group
            live_data = live_data_obj.get_all_status()
            # live_data is list. first item is id name like "Battery Voltage"
            print("id: {}".format(live_data[0]))
            # second item is value like "12.4"
            print("val: {}".format(live_data[1]))
            # third item is unit like "V"
            print("unit: {}".format(live_data[2]))
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
