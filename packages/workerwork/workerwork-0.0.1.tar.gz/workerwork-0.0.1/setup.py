#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: workerwork(workerwork@qq.com)
# Description:

from setuptools import setup, find_packages

setup(
    name = 'workerwork',
    version = '0.0.1',
    keywords='wow',
    description = 'a library for wow Developer',
    license = 'MIT License',
    url = '',
    author = 'workerwork',
    author_email = 'workerwork@qq.com',
    packages = find_packages(),
    include_package_data = True,
    platforms = 'any',
    install_requires = [
        'requests>=2.19.1',
        'pycrypto>=2.6.1',
        'xmltodict>=0.11.0'
        ],
)
