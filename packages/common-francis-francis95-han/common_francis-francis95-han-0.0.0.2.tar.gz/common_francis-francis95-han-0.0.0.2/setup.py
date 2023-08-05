#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" 
@author zhangbohan.dell@gmail.com
@function:
@create 2020/5/10 19:11
"""

# !/usr/bin/env python
from __future__ import print_function
from setuptools import setup, find_packages
import sys

setup(
    name = "common_francis-francis95-han",
    version = "0.0.0.2",
    author = "francis95-han",
    author_email = "zhangbohan.dell@gmail.com",
    description = "python common_francis package",
    long_description = open("README.md").read(),
    license = "MIT",
    url = "https://github.com/francis95-han/common-francis95-han",
    packages = ['common_francis'],
    install_requires = [
    ],
    classifiers = [
    "Environment :: Plugins",
    "Intended Audience :: Developers",
    "Topic :: Text Processing :: Indexing",
    "Topic :: Utilities",
    "Topic :: Internet",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    ],
)