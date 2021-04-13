#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""TS-MPPT-60 driver library to get all devices status data."""

from tsmppt60_driver.base import ManagementBase
from tsmppt60_driver.status import BatteryStatus
from tsmppt60_driver.status import CountersStatus
from tsmppt60_driver.status import SolarArrayStatus
from tsmppt60_driver.status import TemperaturesStatus
from tsmppt60_driver.status import OperatingConditions


class SystemStatus(object):
    """This is class to get the system status of TS-MPPT-60. Use this like below.

        print(SystemStatus("192.168.1.20").get())

        {'Amp Hours': {'group': 'Counter', 'unit': 'Ah', 'value': 18097.9},
         'Array Current': {'group': 'Array', 'unit': 'A', 'value': 1.4},
         'Array Voltage': {'group': 'Array', 'unit': 'V', 'value': 53.41},
         'Battery Voltage': {'group': 'Battery', 'unit': 'V', 'value': 23.93},
         'Charge Current': {'group': 'Battery', 'unit': 'A', 'value': 3.2},
         'Heat Sink Temperature': {'group': 'Temperature', 'unit': 'C', ...},
         'Kilowatt Hours': {'group': 'Counter', 'unit': 'kWh', 'value': 237.0},
         'Target Voltage': {'group': 'Battery', 'unit': 'V', 'value': 28.6}}

    The above data is limited information. You can disable the limitter
    like below.

        print(SystemStatus("192.168.1.20").get(False))

        {'Amp Hours': {'group': 'Counter', 'unit': 'Ah', 'value': 18097.8},
         'Array Current': {'group': 'Array', 'unit': 'A', 'value': 1.3},
         'Array Voltage': {'group': 'Array', 'unit': 'V', 'value': 53.41},
         'Battery Temperature': {'group': 'Temperature', 'unit': 'C', ...},
         'Battery Voltage': {'group': 'Battery', 'unit': 'V', 'value': 24.01},
         'Charge Current': {'group': 'Battery', 'unit': 'A', 'value': 3.2},
         'Heat Sink Temperature': {'group': 'Temperature', 'unit': 'C', ...},
         'Kilowatt Hours': {'group': 'Counter', 'unit': 'kWh', 'value': 237.0},
         'Output Power': {'group': 'Battery', 'unit': 'W', 'value': 76.0},
         'Sweep Pmax': {'group': 'Array', 'unit': 'W', 'value': 73.0},
         'Sweep Vmp': {'group': 'Array', 'unit': 'V', 'value': 53.41},
         'Sweep Voc': {'group': 'Array', 'unit': 'V', 'value': 60.05},
         'Target Voltage': {'group': 'Battery', 'unit': 'V', 'value': 28.6},
         'LED State': {'group': 'Condition', 'value': 11, 'unit': ''},
         'Charge State': {'group': 'Condition', 'value': 3, 'unit': ''}}
    """

    def __init__(self, host):
        """Initialize class object.

        Keyword arguments:
        host -- TS-MPPT-60 host address like "192.168.1.20"
        """
        _mb = ManagementBase(host)

        self._devices = (
            BatteryStatus(_mb),
            SolarArrayStatus(_mb),
            TemperaturesStatus(_mb),
            CountersStatus(_mb),
            OperatingConditions(_mb))

    def get(self, is_limit=True):
        """Get and return all status of devices like the below dict.

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

        Keyword arguments:
        is_limit -- limit the number of getting status
        """
        status_dict = {}

        for device in self._devices:
            for status in device.get_status_all(is_limit):
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
