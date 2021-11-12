#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021.11.03 11:24
@file: __init__.py.py
@Desc：
"""
from .LogPrint import LogPrint
from .Result import Result
from .DealWith import deal_with_bytes_2_str

log_print = LogPrint.log_print
log_for_time = LogPrint.log_for_time
Result = Result
log_for_error = LogPrint.log_for_error
deal_with_bytes_2_str = deal_with_bytes_2_str

if __name__ == '__main__':
    pass
