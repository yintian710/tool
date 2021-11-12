#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021.11.11 08:59
@file: db_tool.py
@Desc：
"""

from .db_dbutils_init import get_my_connection

"""执行语句查询有结果返回结果没有返回0；增/删/改返回变更数据条数，没有返回0"""


class MySqlTool(object):
    def __init__(self):
        self.db = get_my_connection()  # 从数据池中获取连接

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'inst'):  # 单例
            cls.inst = super(MySqlTool, cls).__new__(cls, *args, **kwargs)
        return cls.inst

    # 封装执行命令
    def execute(self, sql, param=None, auto_close=False):
        """
        【主要判断是否有参数和是否执行完就释放连接】
        :param sql: 字符串类型，sql语句
        :param param: sql语句中要替换的参数"select %s from tab where id=%s" 其中的%s就是参数
        :param auto_close: 是否关闭连接
        :return: 返回连接conn和游标cursor
        """
        cursor, conn = self.db.getconn()  # 从连接池获取连接
        count = 0
        try:
            # count : 为改变的数据条数
            if param:
                count = cursor.execute(sql, param)
            else:
                count = cursor.execute(sql)
            conn.commit()
            if auto_close:
                self.close(cursor, conn)
        except Exception as e:
            print(e)
        return cursor, conn, count

    # 执行多条命令
    # def executemany(self, lis):
    #     """
    #     :param lis: 是一个列表，里面放的是每个sql的字典'[{"sql":"xxx","param":"xx"}....]'
    #     :return:
    #     """
    #     cursor, conn = self.db.getconn()
    #     try:
    #         for order in lis:
    #             sql = order['sql']
    #             param = order['param']
    #             if param:
    #                 cursor.execute(sql, param)
    #             else:
    #                 cursor.execute(sql)
    #         conn.commit()
    #         self.close(cursor, conn)
    #         return True
    #     except Exception as e:
    #         print(e)
    #         conn.rollback()
    #         self.close(cursor, conn)
    #         return False

    # 释放连接
    @staticmethod
    def close(cursor, conn):
        """释放连接归还给连接池"""
        cursor.close()
        conn.close()

    # 查询所有
    def select(self, sql, param=None):
        cursor, conn, count = self.execute(sql, param)
        try:
            res = cursor.fetchall()
            return res
        except Exception as e:
            print(e)
            self.close(cursor, conn)
            return count

    # 查询单条
    def select_one(self, sql, param=None):
        cursor, conn, count = self.execute(sql, param)
        try:
            res = cursor.fetchone()
            self.close(cursor, conn)
            return res
        except Exception as e:
            print("error_msg:", e.args)
            self.close(cursor, conn)
            return count

    # 增加
    def insert(self, sql, param):
        cursor, conn, count = self.execute(sql, param)
        try:
            # _id = cursor.lastrowid()  # 获取当前插入数据的主键id，该id应该为自动生成为好
            conn.commit()
            self.close(cursor, conn)
            return count
            # 防止表中没有id返回0
            # if _id == 0:
            #     return True
            # return _id
        except Exception as e:
            print(e)
            conn.rollback()
            self.close(cursor, conn)
            return count

    # 增加多行
    def insert_many(self, sql, param):
        """
        :param sql:
        :param param: 必须是元组或列表[(),()]或（（），（））
        :return:
        """
        cursor, conn, count = self.db.getconn()
        try:
            cursor.executemany(sql, param)
            conn.commit()
            return count
        except Exception as e:
            print(e)
            conn.rollback()
            self.close(cursor, conn)
            return count

    # 删除
    def delete(self, sql, param=None):
        cursor, conn, count = self.execute(sql, param)
        try:
            self.close(cursor, conn)
            return count
        except Exception as e:
            print(e)
            conn.rollback()
            self.close(cursor, conn)
            return count

    # 更新
    def update(self, sql, param=None):
        cursor, conn, count = self.execute(sql, param)
        try:
            conn.commit()
            self.close(cursor, conn)
            return count
        except Exception as e:
            print(e)
            conn.rollback()
            self.close(cursor, conn)
            return count

    @staticmethod
    def __alalis(data):
        if isinstance(data, list):
            for r in data:
                for key in r:
                    if type(r[key]).__name__ == 'str':
                        if r[key] is not None and '\\x' in r[key]:
                            r[key] = bytes(r[key]).decode('utf-8')
                    if type(r[key]).__name__ == 'bytes':
                        r[key] = str(r[key], encoding='utf-8')
        if isinstance(data, dict):
            for key in data:
                if type(data[key]).__name__ == 'str':
                    if data[key] is not None and '\\x' in data[key]:
                        data[key] = bytes(data[key]).decode('utf-8')
                if type(data[key]).__name__ == 'bytes':
                    data[key] = str(data[key], encoding='utf-8')
        return data


db = MySqlTool()
if __name__ == '__main__':
    pass
    # # 查询单条
    # sql1 = 'select * from userinfo where name=%s'
    # args = 'python'
    # ret = db.selectone(sql=sql1, param=args)
    # print(ret)  # (None, b'python', b'123456', b'0')
    # 增加单条
    # sql2 = 'insert into userinfo (name,password) VALUES (%s,%s)'
    # ret = db.insertone(sql2, ('old2','22222'))
    # print(ret)
    # 增加多条
    # sql3 = 'insert into userinfo (name,password) VALUES (%s,%s)'
    # li = li = [
    #     ('分省', '123'),
    #     ('到达','456')
    # ]
    # ret = db.insertmany(sql3,li)
    # print(ret)
    # 删除
    # sql4 = 'delete from  userinfo WHERE name=%s'
    # args = 'xxxx'
    # ret = db.delete(sql4, args)
    # print(ret)
    # 更新
    # sql5 = r'update userinfo set password=%s WHERE name LIKE %s'
    # args = ('993333993', '%old%')
    # ret = db.update(sql5, args)
    # print(ret)
