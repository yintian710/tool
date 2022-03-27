#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021.11.12 15:58
@file: RedisCli.py
@Desc：
"""
import redis

from tool.RedisCli.redis_config import *
from tool.util import deal_with_bytes_2_str


class RedisCli:
    pool = redis.ConnectionPool()

    def __init__(self, db: int = None):
        self.host = HOST
        self.password = PASSWORD
        self.port = PORT
        self.socket_connect_timeout = SOCKET_CONNECT_TIMEOUT
        self.db = DB if db is None else db
        self.max_connections = MAX_CONNECTIONS
        self.to = deal_with_bytes_2_str
        RedisCli.pool = redis.ConnectionPool(
            host=self.host,
            password=self.password,
            port=self.port,
            socket_connect_timeout=self.socket_connect_timeout,
            max_connections=self.max_connections,
            db=self.db
        )
        self.con = redis.Redis(connection_pool=RedisCli.pool)

    def get(self, name):
        res = self.con.get(name)
        res = self.to(res)
        return res


if __name__ == '__main__':
    cls = RedisCli()
    cls.get('1')
