#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021-05-24
@file: base.py
@Desc
"""
import hashlib
import random
from datetime import datetime


class Base:
    def __init__(self, task, nums=None):
        self.nums = nums if nums else random.randint(1000, 9999)
        self.str_ = f'{task}-{self.nums}-{self.__class__.__name__}-'
        self.try_times = 0
        self.return_data = {}
        self.cookies = {}
        self.error_message = ''
        self._print('初始化成功')

    @staticmethod
    def proce_cookies(cookies):
        """
        将cookies字典转换成header字符串
        :param cookies:
        :return:
        """
        c = ''
        for k, _ in cookies.items():
            c += f'{k}={_};'
        return c

    def __str__(self):
        str1 = f'{self.str_}返回数据--->{self.return_data}'
        return str1

    def _print(self, *str1):
        str2 = ''
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for _ in str1:
            str2 += str(_)
        print(f'{self.str_}-{now}-{str2}')

    def call_print(self, *str1):
        self._print(*str1)

    @staticmethod
    def md5(str1):
        md = hashlib.md5()  # 创建md5对象
        md.update(str1.encode(encoding='utf-8'))
        return md.hexdigest()


if __name__ == '__main__':
    pass
