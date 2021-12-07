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

from tool.util import log_print, Result


class BaseCv:
    def __init__(self, task, nums=None):
        self.nums = nums if nums else randint(1000, 9999)
        self.str_ = f'{task}-{self.nums}-{self.__class__.__name__}-'
        self.try_times = 0
        self.error_message = ''
        self.result = Result()
        self._print('初始化成功')

    @staticmethod
    def bytes2cv(img):
        """
        二进制图片转cv2
        :param img: 二进制图片数据，bytes
        :return: cv2图像，numpy.ndarray
        """
        return imdecode(np.array(bytearray(img), dtype='uint8'), cv2.IMREAD_UNCHANGED)

    @staticmethod
    def bytes2b64(img):
        img = base64.b64encode(img)
        return img

    def file2b64(self, path):
        with open(path, 'r') as f:
            img = f.read()
        return self.bytes2b64(img)

    def base642cv(self, img):
        """
        base64转cv2
        :param img: base64图片数据，base64
        :return: cv2图像，numpy.ndarray
        """
        img = base64.b64decode(img)
        img = self.bytes2cv(img)
        return img

    @staticmethod
    def compare_hist(img1, img2):
        img1 = np.float32(img1)
        img2 = np.float32(img2)
        # img1 = np.frombuffer(img1, dtype=np.uint8)
        # img2 = np.frombuffer(img2, dtype=np.uint8)
        img1 = np.ndarray.flatten(img1)
        img2 = np.ndarray.flatten(img2)
        orc = np.corrcoef(img1, img2)
        return orc[0, 1]

    def diff_b64(self, img1_b64, img2_b64):
        img1_b = base64.b64decode(img1_b64)
        img2_b = base64.b64decode(img2_b64)
        img1 = cv2.imdecode(np.array(bytearray(img1_b), dtype='uint8'), cv2.COLOR_RGB2BGR)
        img2 = cv2.imdecode(np.array(bytearray(img2_b), dtype='uint8'), cv2.COLOR_RGB2BGR)
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        # cv2.imwrite('1.png', m)
        cor = self.compare_hist(img1, img2)
        if cor > 0.90:
            # print(cor3)
            return True

    def diff_b(self, img1_b64, img2_b64):
        img1_b = base64.b64decode(img1_b64)
        img2_b = base64.b64decode(img2_b64)
        img1 = cv2.imdecode(np.array(bytearray(img1_b), dtype='uint8'), cv2.COLOR_RGB2BGR)
        img2 = cv2.imdecode(np.array(bytearray(img2_b), dtype='uint8'), cv2.COLOR_RGB2BGR)
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        # cv2.imwrite('1.png', m)
        cor = self.compare_hist(img1, img2)
        if cor > 0.90:
            # print(cor3)
            return True

    def __str__(self):
        str1 = f'{self.str_}'
        return str1

    def call_print(self, *str1):
        self._print(*str1)

    def _print(self, *str1):
        log_print(self.str_, *str1)


if __name__ == '__main__':
    pass
