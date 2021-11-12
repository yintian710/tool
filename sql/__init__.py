#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021.11.10 14:49
@file: __init__.py.py
@Desc：
"""
from tool.sql.db import Mysql
from .connection import get_db, get_cur

get_db = get_db
get_cur = get_cur
db = Mysql()


if __name__ == '__main__':
    pass
