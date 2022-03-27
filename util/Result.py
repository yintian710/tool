#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021.11.03 11:19
@file: Result.py
@Desc：
"""


class Result:
    code: int = 0
    message: str = ''
    need: dict = None

    def bad_result(self, message='', code=1):
        self.code = code
        self.message = message
        return self.__dict__

    def good_result(self, message='', code=0):
        self.code = code
        self.message = message
        return self.__dict__

    def set_need(self, need: dict):
        for k, v in need.items():
            self.__setattr__(str(k), v)

    def dict(self):
        return self.__dict__

    @staticmethod
    def good(message='', code=0):
        return {'message': message, 'code': code}

    @staticmethod
    def bad(message='', code=1):
        return {'message': message, 'code': code}

    def __str__(self):
        return self.__dict__


if __name__ == '__main__':
    pass
