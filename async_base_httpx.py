#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021-05-24
@file: base.py
@Desc
"""
import asyncio
import hashlib
import json
import random
from datetime import datetime

import httpx


class AsyncBaseHttpx:
    def __init__(self, task, nums=None):
        self.session = httpx.AsyncClient()
        self.nums = nums if nums else random.randint(1000, 9999)
        self.str_ = f'{task}-{self.nums}-{self.__class__.__name__}-'
        self.try_times = 0
        self.return_data = {}
        self.cookies = {}
        self.error_message = ''
        self._print('初始化成功')

    async def try_do_func(self, func, max_times=3, *args, ):
        """"""
        times = 0
        while times < max_times:
            times += 1
            try:
                result = await func(*args)
                if result:
                    return result
            except Exception as e:
                self.error_message += f'-{type(e)}-{str(e)}-'
        return False

    async def proce_cookies(self):
        """
        将cookies字典转换成header字符串
        :return:
        """
        c = ''
        for k, _ in self.cookies.items():
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

    def _try_times(self) -> int:
        self.try_times += 1
        return self.try_times - 1

    @staticmethod
    def md5(str1):
        md = hashlib.md5()  # 创建md5对象
        md.update(str1.encode(encoding='utf-8'))
        return md.hexdigest()


async def test():
    AB = AsyncBaseHttpx('test')
    # async with AB.session.get('https://www.baidu.com') as res:
    #     print(await res.text())
    await AB.set_ip()
    await AB.re_session()
    res = await AB.session.get('https://ip.cn/api/index?ip=&type=0')
    print()
    # await AB.session.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
