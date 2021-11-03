#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021-07-08
@file: MqTool.py
@Desc
"""
import functools
import json

from rocketmq.client import Producer, Message

mq_types_dict = {'mq_order': 'sc-test'}


def mq_product(mq_types, result):
    producer = Producer('sc-test')
    producer.set_namesrv_addr('192.168.2.199:9876')
    producer.start()
    msg = Message(mq_types)
    msg.set_keys('1')
    msg.set_tags('2')
    msg.set_body(json.dumps(result))
    ret = producer.send_sync(msg)
    print(ret.status, ret.msg_id, ret.offset)
    producer.shutdown()


# def mq_return():
def mq_return(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        result = method(*args, **kwargs)
        mq_product(mq_types_dict[method.__name__], result)
    return wrapper

    # return decorate


if __name__ == '__main__':
    pass
