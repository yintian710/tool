#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021.11.13 16:14
@file: MerryTool.py
@Desc：
"""
import inspect
from functools import wraps
from typing import Any

from merry import Merry
from .Result import Result

getargspec = None
if getattr(inspect, 'getfullargspec', None):
    getargspec = inspect.getfullargspec
else:
    # this one is deprecated in Python 3, but available in Python 2
    getargspec = inspect.getargspec


class MerryTool(Merry):

    def __init__(self):
        super().__init__()
        self.merry_aio = self.aio_try
        self.merry_except = self._except
        self.merry_try = self._try
        self.merry_finally = self._finally
        self.except_[Exception] = self.process_except

    def aio_try(self, f) -> Any:
        """Decorator that wraps a function in a try block.

        Example usage::

            @merry.aio_try
            async def my_function():
                # do something here
        """

        @wraps(f)
        async def wrapper(*args, **kwargs) -> Any:
            ret = None
            try:
                ret = await f(*args, **kwargs)

                # note that if the function returned something, the else clause
                # will be skipped. This is a similar behavior to a normal
                # try/except/else block.
                if ret is not None:
                    return ret
            except Exception as e:
                # find the best handler for this exception
                handler = None
                for c in self.except_.keys():
                    if isinstance(e, c):
                        if handler is None or issubclass(c, handler):
                            handler = c

                # if we don't have any handler, we let the exception bubble up
                if handler is None:
                    raise e

                # log exception
                # self.logger.exception('[merry] Exception caught')

                # if in debug mode, then bubble up to let a debugger handle
                debug = self.debug
                if handler in self.force_debug:
                    debug = True
                elif handler in self.force_handle:
                    debug = False
                if debug:
                    raise e

                # invoke handler
                if len(getargspec(self.except_[handler])[0]) == 0:
                    return self.except_[handler]()
                else:
                    return self.except_[handler](e)
            else:
                # if we have an else handler, call it now
                if self.else_ is not None:
                    return self.else_()
            finally:
                # if we have a finally handler, call it now
                if self.finally_ is not None:
                    alt_ret = self.finally_()
                    if alt_ret is not None:
                        ret = alt_ret
                    return ret

        return wrapper

    @staticmethod
    def process_except(e):
        return Result.bad(f'程序异常：{str(e)}--{type(e)}')


if __name__ == '__main__':
    pass
