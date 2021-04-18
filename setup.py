#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from setuptools import setup, find_packages


def readme():
    try:
        _r = os.path.join(os.path.dirname(__file__), 'README.rst')
        with open(_r, 'r') as _f:
            return _f.read()
    except:
        return ""


def requires():
    try:
        with open('requirements.txt', 'r') as _f:
            return _f.readlines()
    except:
        return []


setup(
    name="tsmppt60-driver",
    version="0.2.0",
    description="Python module to get status of your solar charge controller TS-MPPT-60.",
    long_description=readme(),
    license="GPLv2",
    author="Takashi Ando",
    author_email="takashi7ando@gmail.com",
    url="https://github.com/dodo5522/tsmppt60_driver",
    install_requires=requires(),
    packages=find_packages(),
    test_suite='nose.collector',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: System :: Hardware :: Hardware Drivers',
    ]
)
