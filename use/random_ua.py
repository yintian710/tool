#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021-09-01
@file: random_ua.py
@Desc
"""
from faker import Faker

ua = Faker()


def random_ua():
    return ua.user_agent()


if __name__ == '__main__':
    pass
