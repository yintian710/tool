#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 8/12/21
@file: util.py
@Desc
"""
import requests
# import win32file
import functools
import re
from random import choice, randint

from apscheduler.schedulers.background import BackgroundScheduler

scheduler1 = BackgroundScheduler()


def get_result(message, code=0, need: dict = None):
    if not need:
        return {"code": code, 'message': message}
    return {"code": code, 'message': message, **need}


def get_pwd(eng_len=4, num_len=3):
    random_str = ''
    eng_str = ['ABCDEFGHIGKLMNOPQRSTUVWXYZ', 'abcdefghigklmnopqrstuvwxyz']
    length1 = 26
    length2 = 10
    str1 = choice(eng_str)
    str2 = '0123456789'
    for i in range(eng_len):
        random_str += str1[randint(0, length1 - 1)]
    for i in range(num_len):
        random_str += str2[randint(0, length2 - 1)]
    return random_str


# 含参数的装饰器
def call_me(func):
    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs):
        self.call_print(f'{func.__name__}执行中...')
        r = await func(self, *args, **kwargs)
        return r

    return wrapper


# def file_is_used(file_name):
#     try:
#         vHandle = win32file.CreateFile(file_name, win32file.GENERIC_READ, 0, None, win32file.OPEN_EXISTING,
#                                        win32file.FILE_ATTRIBUTE_NORMAL, None)
#         return int(vHandle) == win32file.INVALID_HANDLE_VALUE
#     except:
#         return True
#     finally:
#         try:
#             win32file.CloseHandle(vHandle)
#         except:
#             pass


def get_host_ip():
    # url = 'https://ip.cn/api/index?ip=&type=0'
    # headers = {'accept': 'application/json, text/javascript, */*; q=0.01', 'accept-encoding': 'gzip, deflate, br',
    #            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8', 'referer': 'https://ip.cn/',
    #            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
    #            'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'empty',
    #            'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-origin',
    #            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
    #            'x-requested-with': 'XMLHttpRequest'}
    # res = requests.get(url, headers=headers)
    # if res.status_code != 200:
    #     return get_result('获取ip失败', 1)
    # ip = res.json()['ip']
    res = requests.get("http://txt.go.sohu.com/ip/soip")
    res_text = res.text
    ip = re.findall(r'\d+.\d+.\d+.\d+', res_text)
    return ip[0]


if __name__ == '__main__':
    get_host_ip()
