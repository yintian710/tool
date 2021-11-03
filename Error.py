#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021-03-23
@file: Error.py
"""


class ReTryTimesError(Exception):
    def __init__(self, message):
        self.message = message


class TimeOutError(Exception):
    def __init__(self, message):
        self.message = message


class GetIpError(Exception):
    def __init__(self, message):
        self.message = message


class PostError(Exception):
    def __init__(self, message):
        self.message = message


class GetError(Exception):
    def __init__(self, message):
        self.message = message


class LoginError(Exception):
    def __init__(self, message):
        self.message = message


class Login1Error(Exception):
    def __init__(self, message):
        self.message = message


class SelectError(Exception):
    def __init__(self, message):
        self.message = message


class PayError(Exception):
    def __init__(self, message):
        self.message = message


class NeedError(Exception):
    def __init__(self, message):
        self.message = message


class OrderError(Exception):
    def __init__(self, message):
        self.message = message


class IdTypeError(Exception):
    def __init__(self, message):
        self.message = message


class InputError(Exception):
    def __init__(self, message):
        self.message = message


class MoveError(Exception):
    def __init__(self, message):
        self.message = message


class DataError(Exception):
    def __init__(self, message):
        self.message = message


class GetEzPayUrlError(Exception):
    def __init__(self, message):
        self.message = message


class GetOrderDataError(Exception):
    def __init__(self, message):
        self.message = message


class GetCityCodeError(Exception):
    def __init__(self, message):
        self.message = message


class MqValueError(Exception):
    def __init__(self, message):
        self.message = message


class ProceDataError(Exception):
    def __init__(self, message):
        self.message = message
