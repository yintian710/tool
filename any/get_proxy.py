#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021-07-09
@file: get_proxy.py
@Desc
"""

import sys

import requests

_version = sys.version_info

is_python3 = (_version[0] == 3)

ip = "dynamic.xiongmaodaili.com"
# 企业动态按并发
port = 8091

proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": ip,
    "port": port,
    # 下值修改为订单中的用户名
    "user": "xtpa",
    # 下值修改为订单中的密码
    "pass": "qq1174715258",
}
proxy = {"http": proxyMeta, "https": proxyMeta}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36"}
r = requests.get("https://2021.ip138.com", headers=headers, proxies=proxy, verify=False, allow_redirects=False)
r.encoding = 'utf8'
print(r.status_code)
print(r.text)
if r.status_code == 302 or r.status_code == 301:
    loc = r.headers['Location']
    print(loc)
    r = requests.get(loc, headers=headers, proxies=proxy, verify=False, allow_redirects=False)
    r.encoding = 'utf8'
    print(r.status_code)
    print(r.text)

if __name__ == '__main__':
    pass
