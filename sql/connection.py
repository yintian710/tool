#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021.11.10 14:55
@file: connection.py
@Desc：
"""
import pymysql
from pymysql.connections import Connection
from pymysql.cursors import Cursor

from tool.Error import MySqlConnectionError
from tool.version import MYSQL_HOST, MYSQL_USER, MYSQL_DATABASE, MYSQL_PASSWORD, MYSQL_PORT


def get_db() -> Connection:
    try:
        db = pymysql.connect(host=MYSQL_HOST,
                             port=MYSQL_PORT,
                             user=MYSQL_USER,
                             password=MYSQL_PASSWORD,
                             database=MYSQL_DATABASE)
        try:
            yield db
        finally:
            db.close()
    except Exception as e:
        raise MySqlConnectionError(f'connect {MYSQL_HOST} error - {type(e)}--{str(e)}')


def get_cur() -> Cursor:
    db = get_db()
    cur = db.cursor()
    try:
        yield cur
    finally:
        cur.close()


if __name__ == '__main__':
    pass
