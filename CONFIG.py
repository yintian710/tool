#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021-07-08
@file: CONFIG.py.py
@Desc
"""
import os

from tool.version import PROJECT_NAME

path = os.getcwd()
work_path = path.split(PROJECT_NAME)[0]
work_path = os.path.join(work_path, PROJECT_NAME)
tool_path = os.path.join(work_path, 'tool')
json_path = os.path.join(work_path, 'json_data')
file_path = os.path.join(work_path, 'file')

if __name__ == '__main__':
    pass