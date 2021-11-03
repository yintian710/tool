#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021-05-24
@file: base.py
@Desc
"""
import base64
import hashlib
import json
import random
import time
from datetime import datetime

import requests

from tool.Error import GetIpError


class Base:
    def __init__(self, task, nums=None, need_ip=True):
        self.nums = nums if nums else random.randint(1000, 9999)
        self.str_ = f'{task}-{self.nums}-{self.__class__.__name__}-'
        self.ip_times = 0
        self.try_times = 0
        self.return_data = {}
        if need_ip:
            self.pp = self.ti()

    @property
    def set_proxy(self):
        """
        获取代理池IP，一次只能取一个
        :return:
        """
        self.ip_times += 1
        url_pool = 'http://ip.api.xiangshangsl.com/ip/getIp?name=sc'
        try:
            res = requests.get('http://120.76.117.25:8888/count/')
            count = int(res.text)
            if count > 20:
                url_pool = 'http://120.76.117.25:8888/get/'
        except Exception as e:
            pass
        url = "http://api.wandoudl.com/api/ip?app_key=e272230fec2b78a66a63163abf0d6336&pack=207366&" \
              "num=1&xy=1&type=2&lb=\r\n&mr=1&"
        header = {'Connection': 'close',
                  "Proxy-Authorization": "Basic " + base64.b64encode(
                      '2851636003@qq.com:Bw5223591'.encode('utf-8')).decode()}
        get_ip = requests.get(url=url_pool, stream=False, headers=header, timeout=5)
        if get_ip.status_code == 200:
            ip_time = get_ip.json().get('expire_time')
            ip_time = time.mktime(time.strptime(ip_time, '%Y-%m-%d %H:%M:%S'))
            get_ip = get_ip.content.decode()
            ip = json.loads(get_ip)['address']
            port = json.loads(get_ip)['port']
            reip = {'http': ip + ':' + str(port),
                    'https': ip + ':' + str(port),
                    'expire_time': ip_time}
            return reip
        else:
            get_ip = requests.get(url=url, stream=False, header=header, timeout=5).content.decode()
            ip = json.loads(get_ip.content.decode())['data'][0]['ip']
            port = json.loads(get_ip.content.decode())['data'][0]['port']
            reip = {'http': ip + ':' + str(port),
                    'https': + ip + ':' + str(port)}
            return reip

    def ti(self):
        """
        执行det_proxy方法
        :return:
        """
        while self.ip_times < 10:
            now = time.time()
            try:
                pp = self.set_proxy
            except Exception as e:
                self._print(e)
                self.ip_times += 1
                pp = self.ti()
            times = pp.pop('expire_time') - now
            self._print(pp, times)
            if times < 180:
                self.ip_times += 1
                pp = self.ti()
                self.ip_times = 0
                return pp
            else:
                self.ip_times = 0
                return pp
        raise GetIpError('获取ip异常')

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
