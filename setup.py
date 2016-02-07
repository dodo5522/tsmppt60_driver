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


setup(
    name="tsmppt60-driver",
    version="0.1.2",
    description="Python module to get status of your solar charge controller TS-MPPT-60.",
    long_description=readme(),
    license="GPLv2",
    author="Takashi Ando",
    author_email="takashi7ando@gmail.com",
    url="https://github.com/dodo5522/tsmppt60_driver",
    install_requires=[
        'requests>=2.8.0',
    ],
    packages=find_packages(),
    test_suite='nose.collector',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Natural Language :: Japanese',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: System :: Hardware',
        'Topic :: System :: Hardware :: Hardware Drivers',
    ]
)
