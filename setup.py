#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from setuptools import setup

setup(
    name="tsmppt60-driver",
    version="0.0.7",
    description="Python module to get data from TS-MPPT-60.",
    author="Takashi Ando",
    author_email="takashi7ando@gmail.com",
    url="https://github.com/dodo5522/tsmppt60_driver",
    install_requires=[
        "requests>=2.6.0"],
    packages=[
        "tsmppt60_driver"])
