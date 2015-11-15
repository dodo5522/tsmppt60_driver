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
    """ This is class to get the system status of TS-MPPT-60.
        Use this like below.

        print(SystemStatus("192.168.1.20").get())

        {'Amp Hours': {'group': 'Counter', 'unit': 'Ah', 'value': 18097.9},
         'Array Current': {'group': 'Array', 'unit': 'A', 'value': 1.4},
         'Array Voltage': {'group': 'Array', 'unit': 'V', 'value': 53.41},
         'Battery Voltage': {'group': 'Battery', 'unit': 'V', 'value': 23.93},
         'Charge Current': {'group': 'Battery', 'unit': 'A', 'value': 3.2},
         'Heat Sink Temperature': {'group': 'Temperature', 'unit': 'C', 'value': 25.0},
         'Kilowatt Hours': {'group': 'Counter', 'unit': 'kWh', 'value': 237.0},
         'Target Voltage': {'group': 'Battery', 'unit': 'V', 'value': 28.6}}

        The above data is limited information. You can disable the limitter
        like below.

        print(SystemStatus("192.168.1.20", False).get())

        {'Amp Hours': {'group': 'Counter', 'unit': 'Ah', 'value': 18097.8},
         'Array Current': {'group': 'Array', 'unit': 'A', 'value': 1.3},
         'Array Voltage': {'group': 'Array', 'unit': 'V', 'value': 53.41},
         'Battery Temperature': {'group': 'Temperature', 'unit': 'C', 'value': 25.0},
         'Battery Voltage': {'group': 'Battery', 'unit': 'V', 'value': 24.01},
         'Charge Current': {'group': 'Battery', 'unit': 'A', 'value': 3.2},
         'Heat Sink Temperature': {'group': 'Temperature', 'unit': 'C', 'value': 25.0},
         'Kilowatt Hours': {'group': 'Counter', 'unit': 'kWh', 'value': 237.0},
         'Output Power': {'group': 'Battery', 'unit': 'W', 'value': 76.0},
         'Sweep Pmax': {'group': 'Array', 'unit': 'W', 'value': 73.0},
         'Sweep Vmp': {'group': 'Array', 'unit': 'V', 'value': 53.41},
         'Sweep Voc': {'group': 'Array', 'unit': 'V', 'value': 60.05},
         'Target Voltage': {'group': 'Battery', 'unit': 'V', 'value': 28.6}}
    """

    def __init__(self, host, is_limit=True):
        """
        Keyword arguments:
            host: host address like "192.168.1.20"
            is_limit: limit the number of getting status
        """
        _mb = ManagementBase(host)

        self._devices = (
            BatteryStatus(_mb, is_limit),
            SolarArrayStatus(_mb, is_limit),
            TemperaturesStatus(_mb, is_limit),
            CountersStatus(_mb, is_limit))

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
