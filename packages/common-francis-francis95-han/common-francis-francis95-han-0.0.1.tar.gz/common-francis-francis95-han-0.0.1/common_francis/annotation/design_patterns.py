#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" 
@author zhangbohan.dell@gmail.com
@function:
@create 2020/4/6 19:40
"""
import threading


def singleton_with_args(cls):
    _instance_lock = threading.Lock()
    _instance = {}

    def _singleton(*args, **kargs):
        with _instance_lock:
            if cls not in _instance:
                _instance[cls] = {}
            if args not in _instance[cls]:
                _instance[cls][args] = cls(*args, **kargs)
        return _instance[cls][args]

    return _singleton


def singleton(cls):
    _instance_lock = threading.Lock()
    _instance = {}

    def _singleton(*args, **kargs):
        with _instance_lock:
            if cls not in _instance:
                _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton
