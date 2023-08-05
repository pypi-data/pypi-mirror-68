#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" 
@author zhangbohan.dell@gmail.com
@function:
@create 2020/3/26 15:06
"""

import time,os

from common_francis.log import Logger

__all__=["Logger","logger_cls","logger_func"]

log_dir = "log"
if not os.path.exists(log_dir):
    os.mkdir(log_dir)


def logger_func(function):
    def inner(*args,**kwargs):
        _log = Logger.Logger('log/func_.log')
        start = time.time()
        _log.logger.info("{}-方法{}-开始执行".format(time.asctime(time.localtime(start)), function.__name__))
        rs = function(*args, **kwargs)
        end = time.time()
        _log.logger.info("{}-方法{}-执行结束-运行时间{}".format(time.asctime(time.localtime(end)), function.__name__, end - start))
        return rs
    return inner

def logger_cls(cls):
    _log = Logger.Logger('log/cls_{}.log'.format(cls.__name__))
    if not hasattr(cls, '_log'):
        setattr(cls, '_log', _log)
    return cls

