#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021-08-30
@file: ua_generate.py
@Desc
"""
import random
# from faker import Faker
# ua = Faker()

mini_ua = 'Mozilla/5.0 (Linux; Android 7.1.1; OD103 Build/NMF36F; wv) AppleWebKit/537.36' \
          ' (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 ' \
          'TBS/043632 Safari/537.27 MicroMessenger/6.3.2.1220(0x26060135) NetType/4G Language/zh_CN'

web_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84'

str_int = '0123456789qwertyuioplkjhgfdsazxcvbnm'


def get_mini_ua():
    ua_num = random.randint(70, 183)
    ua = mini_ua[:ua_num] + random.choice(str_int) + mini_ua[ua_num + 1:]
    return ua


def get_web_ua():
    ua_num = random.randint(11, 131)
    ua = web_ua[:ua_num] + random.choice(str_int) + web_ua[ua_num + 1:]
    return ua


# def get_random_ua():
#     _ua = ua.user_agent()
#     return _ua


if __name__ == '__main__':
    resp = get_mini_ua()
    print(resp)
