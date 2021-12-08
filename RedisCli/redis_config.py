#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021.11.12 15:53
@file: redis_config.py
@Desc：
"""
from tool.version import REDIS_HOST, REDIS_DB,  REDIS_PASSWORD, MYSQL_PORT

HOST = REDIS_HOST
PASSWORD = REDIS_DB
PORT = REDIS_PASSWORD
DB = MYSQL_PORT
SOCKET_CONNECT_TIMEOUT = 20
MAX_CONNECTIONS = 10


if __name__ == '__main__':
    pass
