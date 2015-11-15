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

        system_status= SystemStatus("192.168.1.20").get()

        # get() method returns dict and you can parse it like below.
        for key, data in system_status.items():
            # get element name. (like "Battery Voltage", ...)
            elem = key
            # get group. (like "Battery", "Array", ...)
            group = data["group"]
            # get value. (like 24.1[V])
            value = data["value"]
            # get unit. (like "kWh")
            unit = data["unit"]
    """

    def __init__(self, host):
        _mb = ManagementBase(host)

        self._devices = (
            BatteryStatus(_mb),
            SolarArrayStatus(_mb),
            TemperaturesStatus(_mb),
            CountersStatus(_mb))

    def get(self):
        """ Get all status of devices.

        Returns:
            {
                "Battery Voltage":{
                    "group": "Battery",
                    "value": 12.1,
                    "unit": "V"},
                "Charge Current":{
                    "group": "Battery",
                    "value": 8.4,
                    "unit": "A"}
            }
        """
        status_dict = {}

        for device in self._devices:
            for status in device.get_status_all():
                label = status.pop("label")
                status_dict[label] = status

        return status_dict

    def __len__(self):
        return len(self._devices)

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index >= len(self._devices):
            raise StopIteration

        stat_obj = self._devices[self._index]
        self._index += 1

        return stat_obj
