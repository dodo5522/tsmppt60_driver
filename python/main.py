#!/usr/bin/env python3
# -*- coding:utf-8 -*-

""" This is main program to test another modules. """

__author__ = "Takashi Ando"
__copyright__ = "Copyright 2015, My own project"
__credits__ = ["My wife"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Takashi Ando"
__email__ = "noreply@temp.com"
__status__ = "Production"

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        from data.mb import ManagementBase

        mb = ManagementBase()
        print(mb.iscale)
        print(mb.vscale)
        print(mb.read_modbus(address=38, register=1))
        print(mb.read_modbus(address=58, register=1))
        print(mb.read_modbus(address=27, register=1))
        print(mb.read_modbus(address=29, register=1))
    else:
        from data import data

        live = data.LiveData()
        for v in live._data_objects:
            for val in live._data_objects[v].get_all_value():
                print(val)
