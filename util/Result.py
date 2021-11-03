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

    def bad_result(self, message='', code=1):
        self.code = code
        self.message = message

    def good_result(self, message='', code=0):
        self.code = code
        self.message = message

    def dict(self):
        return self.__dict__


if __name__ == '__main__':
    pass
