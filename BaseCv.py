#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021/12/7 19:05
@file: BaseCv.py
@Desc：
"""
import base64
from random import randint
import numpy as np

from cv2 import imdecode, imread, Canny, cvtColor, matchTemplate, minMaxLoc, rectangle, \
    imwrite, COLOR_GRAY2RGB, TM_CCOEFF_NORMED, cv2, resize

from tool.util import log_print


class BaseCv:
    def __init__(self, task, nums=None):
        self.nums = nums if nums else randint(1000, 9999)
        self.str_ = f'{task}-{self.nums}-{self.__class__.__name__}-'
        self.try_times = 0
        self.return_data = {}
        self.cookies = {}
        self.error_message = ''
        self._print('初始化成功')

    @staticmethod
    def bytes2cv(img):
        """
        二进制图片转cv2
        :param img: 二进制图片数据，bytes
        :return: cv2图像，numpy.ndarray
        """
        return imdecode(np.array(bytearray(img), dtype='uint8'), cv2.IMREAD_UNCHANGED)

    def base642cv(self, img):
        """
        base64转cv2
        :param img: base64图片数据，base64
        :return: cv2图像，numpy.ndarray
        """
        img = base64.b64decode(img)
        img = self.bytes2cv(img)
        return img

    def __str__(self):
        str1 = f'{self.str_}返回数据--->{self.return_data}'
        return str1

    def _print(self, *str1):
        log_print(self.str_, *str1)


if __name__ == '__main__':
    pass
