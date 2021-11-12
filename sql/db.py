# coding=utf-8
import pymysql

import MySQLdb

from pymysql.cursors import DictCursor
from dbutils.pooled_db import PooledDB

from . import db_config as config
from ..util import deal_with_bytes_2_str, log_for_error, log_print


class Mysql(object):
    """
    MYSQL数据库对象，负责产生数据库连接 , 此类中的连接采用连接池实现获取连接对象：conn = Mysql.getConn()
            释放连接对象;conn.close()或del conn
    """
    # 连接池对象
    __pool = None

    def __init__(self):
        # 数据库构造函数，从连接池中取出连接，并生成操作游标
        try:
            self._conn = Mysql.__get_onn()
            self._cursor = self._conn.cursor()
        except Exception as e:
            error = f'Connect failed! ERROR {type(e)}-{str(e)}'
            print(error)

    @staticmethod
    def __get_onn():
        """
        @summary: 静态方法，从连接池中取出连接
        @return MySQLdb.connection
        """
        if Mysql.__pool is None:
            __pool = PooledDB(
                creator=config.DB_CREATOR,
                mincached=config.DB_MIN_CACHED,
                maxcached=config.DB_MAX_CACHED,
                maxshared=config.DB_MAX_SHARED,
                maxconnections=config.DB_MAX_CONNECYIONS,
                blocking=config.DB_BLOCKING,
                maxusage=config.DB_MAX_USAGE,
                setsession=config.DB_SET_SESSION,
                host=config.DB_TEST_HOST,
                port=config.DB_TEST_PORT,
                user=config.DB_TEST_USER,
                passwd=config.DB_TEST_PASSWORD,
                db=config.DB_TEST_DBNAME,
                use_unicode=False,
                charset=config.DB_CHARSET
            )
        else:
            __pool = Mysql.__pool
        return __pool.connection()

        # 针对读操作返回结果集

    def _execute(self, sql=''):
        try:
            self._cursor.execute(sql)
            records = self._cursor.fetchall()
            records = list(records)
            return self.__alalis(records)
        except MySQLdb.Error as e:
            log_for_error('MySQL execute failed! ERROR', e)

            # 针对更新,删除,事务等操作失败时回滚

    def _execute_commit(self, sql='', arg=None):
        try:
            if arg is None:
                self._cursor.execute(sql)
            else:
                self._cursor.execute(sql, arg)
            self._conn.commit()
        except MySQLdb.Error as e:
            self._conn.rollback()
            error = 'MySQL execute failed! ERROR (%s): %s' % (e.args[0], e.args[1])
            print(error)
            # sys.exit()

    # 创建表
    # tablename:表名称,attr_dict:属性键值对,constraint:主外键约束
    # attr_dict:{'book_name':'varchar(200) NOT NULL'...}
    # constraint:PRIMARY KEY(`id`)
    def _create_table(self, table, attr_dict, constraint):
        sql = ''
        # sql_mid = '`row_id` bigint(11) NOT NULL AUTO_INCREMENT,'
        sql_mid = ''
        for attr, value in attr_dict.items():
            sql_mid = sql_mid + '`' + attr + '`' + ' ' + value + ','
        sql = sql + 'CREATE TABLE IF NOT EXISTS %s (' % table
        sql = sql + sql_mid
        sql = sql + constraint
        sql = sql + ') ENGINE=InnoDB DEFAULT CHARSET=utf8'
        print('_createTable:' + sql)
        self._execute_commit(sql)

    def insert_one(self, sql, value=None):
        """
        @summary: 向数据表插入一条记录
        @param sql:要插入的ＳＱＬ格式
        @param value:要插入的记录数据tuple/list
        @return: insertId 受影响的行数
        """
        self._execute_commit(sql, value)
        return self.__get_insert_id()

    def _insert(self, table, attrs, value):
        """
        @summary: 向数据表插入一条记录
        @param attrs = [] :要插入的属性
        @param value = [] :要插入的数据值
        """
        # values_sql = ['%s' for v in attrs]
        attrs_sql = '(' + ','.join(attrs) + ')'
        value_str = self._transfer_content(value)
        values_sql = ' values(' + value_str + ')'
        sql = 'insert into %s' % table
        sql = sql + attrs_sql + values_sql
        print('_insert:' + sql)
        self._execute_commit(sql)

    def _insert_dic(self, table, attrs):
        """
        @summary: 向数据表插入一条记录
        @param attrs = {"colNmae:value"} :要插入的属性：数据值
        """
        attrs_sql = '(' + ','.join(attrs.keys()) + ')'
        value_str = self._transfer_content(attrs.values())  # ','.join(attrs.values())
        values_sql = ' values(' + value_str + ')'
        sql = 'insert into %s' % table
        sql = sql + attrs_sql + values_sql
        print('_insert:' + sql)
        self._execute_commit(sql)

        # 将list转为字符串

    @staticmethod
    def _transfer_content(content):
        if content is None:
            return None
        else:
            str_tmp = ""
            for col in content:
                if str_tmp == "":
                    str_tmp = "\"" + col + "\""
                else:
                    str_tmp += "," + "\"" + col + "\""
            return str_tmp

    def _insert_many(self, table, attrs, values):
        """
        @summary: 向数据表插入多条数据
        @param attrs = [id,name,...]  :要插入的属性
        @param values = [[1,'jack'],[2,'rose']] :要插入的数据值
        """
        values_sql = ['%s' * len(attrs)]
        attrs_sql = '(' + ','.join(attrs) + ')'
        values_sql = ' values(' + ','.join(values_sql) + ')'
        sql = 'insert into %s' % table
        sql = sql + attrs_sql + values_sql
        print('_insertMany:' + sql)
        try:
            for i in range(0, len(values), 20000):
                self._cursor.executemany(sql, values[i:i + 20000])
                self._conn.commit()
        except MySQLdb.Error as e:
            self._conn.rollback()
            error = '_insertMany executemany failed! ERROR (%s): %s' % (e.args[0], e.args[1])
            print(error)

    def insert_many(self, sql, values=None):
        """
        @summary: 向数据表插入多条记录
        @param sql:要插入的ＳＱＬ格式
        @param values:要插入的记录数据tuple(tuple)/list[list]
        @return: count 受影响的行数
        """
        try:
            if values is None:
                count = self._cursor.executemany(sql)
            else:
                count = self._cursor.execute(sql, values)
            self._conn.commit()
        except MySQLdb.Error as e:
            self._conn.rollback()
            error = 'MySQL execute failed! ERROR (%s): %s' % (e.args[0], e.args[1])
            print(error)
            count = 0
        return count

    def select(self, sql):
        log_print(sql)
        result = self._execute(sql)
        return self.__alalis(result)

    def __get_insert_id(self):
        """
        获取当前连接最后一次插入操作生成的id,如果没有则为０
        """
        self._cursor.execute("SELECT @@IDENTITY AS id")
        result = self._cursor.fetchall()
        return result[0]['id']

    def __query(self, sql, param=None):
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        return self.__alalis(count)

    def get_all(self, sql, param=None):
        """
        @summary: 执行查询，并取出所有结果集
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list(字典对象)/boolean 查询到的结果集
        """
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        if count > 0:
            result = self._cursor.fetchall()
        else:
            result = False
        return self.__alalis(result)

    def get_one(self, sql, param=None):
        """
        @summary: 执行查询，并取出第一条
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list/boolean 查询到的结果集
        """
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        if count > 0:
            result = self._cursor.fetchone()
        else:
            result = False
        return self.__alalis(result)

    def get_many(self, sql, num, param=None):
        """
        @summary: 执行查询，并取出num条结果
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param num:取得的结果条数
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list/boolean 查询到的结果集
        """

        count = self.__query(sql, param)
        if count > 0:
            result = self._cursor.fetchmany(num)
        else:
            result = False
        return self.__alalis(result)

    def update(self, sql, param=None):
        """
        @summary: 更新数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要更新的  值 tuple/list
        @return: count 受影响的行数
        """
        return self._execute_commit(sql, param)

    def delete(self, sql, param=None):
        """
        @summary: 删除数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要删除的条件 值 tuple/list
        @return: count 受影响的行数
        """
        return self._execute_commit(sql, param)

    def begin(self):
        """
        @summary: 开启事务
        """
        self._conn.autocommit(0)

    def end(self, option='commit'):
        """
        @summary: 结束事务
        """
        if option == 'commit':
            self._conn.commit()
        else:
            self._conn.rollback()

    def dispose(self, is_end=1):
        """
        @summary: 释放连接池资源
        """
        if is_end == 1:
            self.end('commit')
        else:
            self.end('rollback')
        self._cursor.close()
        self._conn.close()

    @staticmethod
    def __alalis(data):
        return deal_with_bytes_2_str(data)

