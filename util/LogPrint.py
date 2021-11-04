#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021.11.04 08:56
@file: LogPrint.py
@Desc：
"""
import logging
import sys
from datetime import datetime, timezone
from pytz import timezone as tz


class LogPrint(logging.Logger):
    @staticmethod
    def log_print(*objects, sep=' ', end='\n', file=sys.stdout, flush=False):
        print("当前时间：" + datetime.now().strftime('%Y-%m-%d %H:%M:%S'), end=' ')  # 这样每次调用log_print()的时候，会先输出当前时间，然后再输出内容
        print(*objects, sep=sep, end=end, file=file, flush=flush)

    @staticmethod
    def log_for_time():
        now = datetime.now().replace(tzinfo=timezone.utc).astimezone(tz=tz('Asia/Shanghai'))
        print("当前时间：" + now.strftime('%Y-%m-%d %H:%M:%S'))


if __name__ == '__main__':
    LogPrint.log_print({123}, 234, 'qwe')
