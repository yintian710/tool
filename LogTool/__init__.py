#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021.11.13 20:36
@file: __init__.py.py
@Desc：
"""
from LogTool import LoggerWrapper

SpiderLogger = LoggerWrapper()
logger = SpiderLogger.get_logger
debug = SpiderLogger.debug
info = SpiderLogger.info
error = SpiderLogger.error
warning = SpiderLogger.warn
exception = SpiderLogger.exception


if __name__ == '__main__':
    pass
