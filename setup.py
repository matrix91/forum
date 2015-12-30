#!/usr/bin/python3
# Copyright (c) 2015 Mattia Setzu
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from setuptools import find_packages
from setuptools import setup

setup(name='forum',
	version='0.1',
	description='Forum dapp library',
	author='Mattia Setzu',
	setup_requires='setuptools',
	author_email='xxx@gmail.com',
	package_dir={'':'library'},
	packages=['forum']
)
