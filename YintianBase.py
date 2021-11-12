#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021.11.11 13:48
@file: YintianBase.py
@Desc：
"""
from typing import Union

from requests import Response

from tool.Error import LoginError
from tool.base import Base
from tool.sql.test import db
from tool.util import log_for_error


class YintianBase(Base):
    def __init__(self, task, nums=None, url_type: Union[int, str] = 0):
        """

        :param task: 任务名
        :param nums: 任务id
        :param url_type: 0为线上，1为本地，其余则是url
        """
        super().__init__(task, nums)
        self.db = db
        self.headers = {
            "Content-Type": "application/json"
        }
        if url_type == 0:
            self.url = 'http://tool.yintian.icu:7100'
        elif url_type == 1:
            self.url = 'http://localhost:7100'
        else:
            self.url = url_type
        self.login()

    def login(self):
        url = '/login'
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
        }
        data = 'grant_type=password&username=yintian&password=yintian'
        res = self.request(url, data, headers)
        if res.status_code != 200:
            raise LoginError('login for yintian error')
        res_json = res.json()
        self.headers['Authorization'] = f'{res_json["token_type"]} {res_json["access_token"]}'
        print()

    def request(self, url: str, data: Union[str, dict], headers=None, **kwargs) -> Response:
        headers = headers if headers else self.headers
        url = self.url + url
        data = data
        if isinstance(data, dict):
            res = self.session.post(url, json=data, headers=headers, **kwargs)
        else:
            res = self.session.post(url, data=data, headers=headers, **kwargs)
        return res


if __name__ == '__main__':
    cls = YintianBase('login')
