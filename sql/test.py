# coding=utf-8
import pymysql

from tool.sql import Mysql

if __name__ == '__main__':
    db = Mysql()
    res = db.select("select * from user where username='yintian'")
    print()
