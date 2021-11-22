#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021.11.13 20:36
@file: LogTool.py
@Desc：
"""
import logging
# -*- coding: utf-8 -*-
# create by yihui 11:32 18/12/19
import logging
import os
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

from tool.CONFIG import log_path
from tool.sql import Mysql


def get_now(string=1):
    now = datetime.now()
    if string:
        return now.strftime('%Y-%m-%d %H:%M:%S')
    return now


class LoggerWrapper:
    def __init__(self, console_init=False):
        self._logger = {}
        self._console_init = console_init
        self.path = log_path
        self.log_name = 'default'
        self.action = 'default'

    @staticmethod
    def _get_path(action, path=""):
        """
        根据日志名，创建对应的日志路径
        :param path:
        :return:
        """
        if action != 'logs':
            action = "logs/" + action + "/"

        path = os.path.join(log_path, action, path)
        if not os.path.exists(path):
            # 当目录不存在时，主动创建
            os.makedirs(path)

        return path

    def _gen_logger(self, action='logs', log_name='default', level=logging.INFO):
        base_logger = logging.getLogger(log_name)
        base_logger.setLevel(level)

        log_file = self._get_path(action, log_name) + "/" + log_name + ".log"
        ch = TimedRotatingFileHandler(log_file, when='D', encoding="utf-8")
        ch.setLevel(level)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        base_logger.addHandler(ch)
        base_logger.propagate = 0

        if not self._console_init:
            console = logging.StreamHandler()
            console.setLevel(logging.DEBUG)
            console.setFormatter(formatter)
            base_logger.addHandler(console)
            self._console_init = True

        return base_logger

    def get_logger(self, action=None, path=None, level=logging.INFO):
        action = action if action else self.action
        if action not in self._logger:
            path = path if path else self.log_name
            self._logger[action] = self._gen_logger(action, path, level)
        return self._logger[action]

    def error(self, msg, name=None, path=None, level=logging.ERROR):
        log = self.get_logger(name, path, level)
        log.error(msg)

    def warn(self, msg, name=None, path=None, level=logging.WARN):
        log = self.get_logger(name, path, level)
        log.warning(msg)

    def info(self, msg, name=None, path=None, level=logging.INFO):
        log = self.get_logger(name, path, level)
        log.info(msg)

    def debug(self, msg, name=None, path=None, level=logging.DEBUG):
        log = self.get_logger(name, path, level)
        log.debug(msg)

    def exception(self, msg, name=None, path=None, level=logging.INFO):
        """
        打印堆栈信息
        :param level:
        :param path:
        :param msg:
        :param name:
        :return:
        """
        log = self.get_logger(name, path, level)
        log.exception(msg)

    def login(self, username, user_id, res=''):
        self.info(f'用户{username}登陆！', name='login', path=username)
        db = Mysql()
        sql = f"insert into log (operation, result, user_id, log_time, result_time) value ('login', '{res}', '{user_id}', '{get_now()}', '{get_now()}')"
        db.insert_one(sql)

    def dk(self, username, user_id, res=''):
        self.info(f'用户{username}dk！', name='dk', path=username)
        db = Mysql()
        sql = f"insert into log (operation, result, user_id, log_time, result_time) value ('dk', '{res}', '{user_id}', '{get_now()}', '{get_now()}')"
        db.insert_one(sql)


if __name__ == '__main__':
    lohs = LoggerWrapper()
    lohs.login('yintian', '100001')
