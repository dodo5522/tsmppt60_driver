#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from setuptools import setup


def readme():
    try:
        os.system("pandoc --from=markdown --to=rst README.md -o README.rst")
        with open("README.rst", "r") as f:
            return f.read()
    except:
        return ""

setup(
    name="tsmppt60-driver",
    version="0.0.7",
    description="To get status of your solar charge controller TS-MPPT-60.",
    long_description=readme(),
    license="GPLv2",
    author="Takashi Ando",
    author_email="takashi7ando@gmail.com",
    url="https://github.com/dodo5522/tsmppt60_driver",
    install_requires=[
        "requests>=2.6.0"],
    packages=[
        "tsmppt60_driver"])
