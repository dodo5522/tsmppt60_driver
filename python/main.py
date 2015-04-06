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
    from driver import data

    url = sys.argv[1]

    live = data.LiveData(url)
    for group in live._data_objects:
        for data_in_group in live._data_objects[group].get_all():
            print(data_in_group)
