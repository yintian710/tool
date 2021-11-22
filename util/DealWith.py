#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021.11.11 11:28
@file: DealWith.py
@Desc：
"""


def deal_with_bytes_2_str(data):
    if isinstance(data, (set, list, tuple)):
        res = []
        for _ in data:
            res.append(deal_with_bytes_2_str(_))
        return res
    elif isinstance(data, dict):
        res = dict()
        for k, v in data.items():
            res[deal_with_bytes_2_str(k)] = deal_with_bytes_2_str(v)
        return res
    elif isinstance(data, bytes):
        return data.decode()
    else:
        return data


if __name__ == '__main__':
    print(deal_with_bytes_2_str(''))
