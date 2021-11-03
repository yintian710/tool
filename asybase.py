#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021-05-24
@file: base.py
@Desc
"""
import asyncio
import base64
# import json
import hashlib
import json
import random
import time
from datetime import datetime

import aiohttp
from jsonpath import jsonpath
import requests

from tool.Error import GetIpError


class AsyncBase:
    pp: str = ''

    def __init__(self, task, nums=None):
        self.session = aiohttp.ClientSession()
        self.nums = nums if nums else random.randint(1000, 9999)
        self.str_ = f'{task}-{self.nums}-{self.__class__.__name__}-'
        self.ip_times = 0
        self.try_times = 0
        self.return_data = {}
        self.cookies = {}
        self.error_message = ''
        self._print('初始化成功')

    async def try_do_func(self, func, max_times=3, good=0, *args, ):
        """"""
        times = 0
        while times < max_times:
            times += 1
            try:
                await self.set_ip(good)
                result = await func(*args)
                if result:
                    return result
            except Exception as e:
                self.error_message += f'-{type(e)}-{str(e)}-'
        return False

    async def re_session(self):
        await self.session.close()
        self.session = aiohttp.ClientSession()

    async def set_ip(self, good=0):
        # await self.session.close()
        # self.session = aiohttp.ClientSession()
        if not good:
            pp = await self.ti()
        else:
            self.try_times = 0
            pp = await self.good_proxy()
            # start, res = await self.get_ping(pp)
            # a = res[0]
            # ping = (time.time() - start) * 1000
            # self._print(pp, '-', ping)
            # while ping > 500 and self.try_times < 10:
            #     pp = await self.good_proxy()
            #     start, res = await self.get_ping(pp)
            #     a = res[0]
            #     ping = (time.time() - start) * 1000
            #     self._print(pp, '-', ping)
        self._print(pp)
        self.pp = pp['http']

    async def set_proxy(self):
        """
        获取代理池IP，一次只能取一个
        :return:
        """
        self.ip_times += 1
        url_pool = 'http://ip.api.xiangshangsl.com/ip/getIp?name=sc&source=ty'
        # try:
        #     count_url = 'http://120.76.117.25:8888/count/'
        #     # res = await self.get_text(count_url)
        #     res = await self.session.get(count_url)
        #     count = int(await res.text())
        #     if count > 20:
        #         url_pool = 'http://120.76.117.25:8888/get/'
        # except Exception as e:
        #     print(e)
        # url = "http://api.wandoudl.com/api/ip?app_key=e272230fec2b78a66a63163abf0d6336&pack=207366&" \
        #       "num=1&xy=1&type=2&lb=\r\n&mr=1&"
        headers = {'Connection': 'close',
                   "Proxy-Authorization": "Basic " + base64.b64encode(
                       '2851636003@qq.com:Bw5223591'.encode('utf-8')).decode()}
        # self.session.headers.update(headers)
        get_ip = await self.session.get(url_pool, headers=headers)
        # get_ip = requests.get(url=url_pool, stream=False, headers=header, timeout=5)
        # if get_ip.status == 200:
        ip_json = await get_ip.text()
        ip_json = json.loads(ip_json)
        ip_time = ip_json.get('expire_time')
        ip_time = time.mktime(time.strptime(ip_time, '%Y-%m-%d %H:%M:%S'))
        ip = ip_json['address']
        port = ip_json['port']
        now = time.time()
        out_time = ip_time - now
        reip = {'http': "http://" + ip + ':' + str(port),
                'https': "https://" + ip + ':' + str(port),
                'source': ip_json['source'],
                'expire_time': ip_time,
                'out_time': out_time}

        return reip
        # else:
        #     async with self.session.get(url, headers=headers) as res:
        #         get_ip = res
        #         # get_ip = requests.get(url=url, stream=False, header=header, timeout=5).content.decode()
        #         ip_json = await get_ip.text()
        #         ip_json = json.loads(ip_json)
        #         ip = ip_json['data'][0]['ip']
        #         port = ip_json['data'][0]['port']
        #         ip_time = ip_json.get('expire_time')
        #         ip_time = time.mktime(time.strptime(ip_time, '%Y-%m-%d %H:%M:%S'))
        #         reip = {'http': "http://" + ip + ':' + str(port),
        #                 'https': "https://" + ip + ':' + str(port),
        #                 'expire_time': ip_time}
        #         return reip

    async def good_proxy(self):
        """
        获取代理池IP，一次只能取一个
        :return:
        """
        self.ip_times += 1
        url_pool = 'http://ip.api.xiangshangsl.com/ip/getIp?name=sc&source=ty'
        try:
            count_url = 'http://120.76.117.25:8888/count/'
            # res = await self.get_text(count_url)
            res = await self.session.get(count_url)
            count = int(await res.text())
            if count > 20:
                url_pool = 'http://120.76.117.25:8888/get/'
        except Exception as e:
            print(e)
        url = "http://api.wandoudl.com/api/ip?app_key=e272230fec2b78a66a63163abf0d6336&pack=207366&" \
              "num=1&xy=1&type=2&lb=\r\n&mr=1&"
        headers = {'Connection': 'close',
                   "Proxy-Authorization": "Basic " + base64.b64encode(
                       '2851636003@qq.com:Bw5223591'.encode('utf-8')).decode()}
        self.session.headers.update(headers)
        get_ip = await self.session.get(url_pool, headers=headers)
        # get_ip = requests.get(url=url_pool, stream=False, headers=header, timeout=5)
        if get_ip.status == 200:
            ip_json = await get_ip.text()
            ip_json = json.loads(ip_json)
            ip_time = ip_json.get('expire_time')
            ip_time = time.mktime(time.strptime(ip_time, '%Y-%m-%d %H:%M:%S'))
            ip = ip_json['address']
            port = ip_json['port']
            now = time.time()
            out_time = ip_time - now
            reip = {'http': "http://" + ip + ':' + str(port),
                    'https': "https://" + ip + ':' + str(port),
                    'source': ip_json['source'],
                    'expire_time': ip_time,
                    'out_time': out_time}
        else:
            async with self.session.get(url, headers=headers) as res:
                get_ip = res
                # get_ip = requests.get(url=url, stream=False, header=header, timeout=5).content.decode()
                ip_json = await get_ip.text()
                ip_json = json.loads(ip_json)
                ip = ip_json['data'][0]['ip']
                port = ip_json['data'][0]['port']
                ip_time = ip_json.get('expire_time')
                ip_time = time.mktime(time.strptime(ip_time, '%Y-%m-%d %H:%M:%S'))
                now = time.time()
                out_time = ip_time - now
                reip = {'http': "http://" + ip + ':' + str(port),
                        'https': "https://" + ip + ':' + str(port),
                        'source': ip_json['source'],
                        'expire_time': ip_time,
                        'out_time': out_time}
        # self._print(reip)
        if out_time < 200:
            reip = await self.good_proxy()
        return reip

    async def get_ping(self, pp):
        start = time.time()
        res = await self.session.post('http://www.baidu.com/', proxy=pp['http'], ssl=False)
        res_test = await res.text()
        return start, res_test

    async def ti(self):
        """
        执行det_proxy方法
        :return:
        """
        while self.ip_times < 10:
            now = time.time()
            try:
                pp = await self.set_proxy()
            except Exception as e:
                self._print(e)
                self.ip_times += 1
                pp = await self.ti()
            times = pp.pop('expire_time') - now
            # self._print(pp, times)
            if times < 180:
                self.ip_times += 1
                pp = await self.ti()
                self.ip_times = 0
                return pp
            else:
                self.ip_times = 0
                return pp
        raise GetIpError('获取ip异常')

    async def proce_cookies(self):
        """
        将cookies字典转换成header字符串
        :return:
        """
        c = ''
        for k, _ in self.cookies.items():
            c += f'{k}={_};'
        return c

    def log_error(self, text):
        try:
            userMessage = jsonpath(json.loads(text), '$..userMessage')
            if userMessage:
                if ['请验证通过后继续查询'] != userMessage:
                    self.error_message += ' ' + str(userMessage)
        except Exception as e:
            pass

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
    AB = AsyncBase('test')
    # async with AB.session.get('https://www.baidu.com') as res:
    #     print(await res.text())
    await AB.set_ip()
    print()
    # await AB.session.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
