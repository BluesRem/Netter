import copy
import os
import sys
from contextlib import contextmanager, ContextDecorator
from typing import Any

from loguru import logger

Collection = False
Logs = []

__all__ = ['Logger', 'collection']

LEVEL = {
    'TRACE', 5,
    'DEBUG', 10,
    'INFO', 20,
    'SUCCESS', 25,
    'WARNING', 30,
    'ERROR', 40,
    'CRITICAL', 50
}


class Logger(object):

    # 日志设置
    @classmethod
    def initial(cls, level='DEBUG', logfile=None, stdout=True):
        """
        初始化日志记录器
        :return:
        """
        handlers = []
        if stdout:
            handlers.append(dict(sink=sys.stderr, level=level))
        if logfile:
            if os.path.isfile(logfile):
                os.remove(logfile)
            handlers.append(dict(sink=logfile, encoding='UTF-8', level=level))
        logger.configure(
            handlers=handlers
        )

    @classmethod
    def close(cls, name='soium'):
        """
        关闭日志记录
        :return:
        """
        cls.debug('关闭日志记录')
        logger.disable(name)

    @classmethod
    def start(cls, name='soium'):
        """
        开启日志记录
        :return:
        """
        cls.debug('开启日志记录')
        logger.enable(name)

    @classmethod
    @contextmanager
    def pause(cls, name='soium'):
        """
        临时暂停日志记录
        :param name:
        :return:
        """
        cls.close(name=name)
        yield
        cls.start(name=name)

    @classmethod
    def trace(cls, message, *args, **kwargs):
        cls.output(message=message, level=5, *args, **kwargs)

    @classmethod
    def debug(cls, message, *args, **kwargs):
        cls.output(message=message, level=10, *args, **kwargs)

    @classmethod
    def info(cls, message, *args, **kwargs):
        cls.output(message=message, level=20, *args, **kwargs)

    @classmethod
    def success(cls, message, *args, **kwargs):
        cls.output(message=message, level=25, *args, **kwargs)

    @classmethod
    def warning(cls, message, *args, **kwargs):
        cls.output(message=message, level=30, *args, **kwargs)

    @classmethod
    def error(cls, message, *args, **kwargs):
        cls.output(message=message, level=40, *args, **kwargs)

    @classmethod
    def critical(cls, message, *args, **kwargs):
        cls.output(message=message, level=50, *args, **kwargs)

    @classmethod
    def output(cls, message, level: Any = 10, *args, **kwargs):
        global Collection
        if isinstance(level, str):
            level = LEVEL.__getattribute__(level)
        if level == 5:
            output = logger.trace
        elif level == 10:
            output = logger.debug
        elif level == 20:
            output = logger.info
        elif level == 25:
            output = logger.success
        elif level == 30:
            output = logger.warning
        elif level == 40:
            output = logger.error
        elif level == 50:
            output = logger.critical
        else:
            raise ValueError('请输入正确的Level!')
        if Collection:
            Logs.append(message.format(*args, **kwargs))
        else:
            output(message, *args, **kwargs)


class collection(ContextDecorator):
    def __init__(self, level=10):
        self.end = False
        self.level = level
        self.retrying = False
        self.collection = []

    def __enter__(self):
        global Collection
        if not Collection:
            Collection = True
            self.end = True
        else:
            self.collection = copy.deepcopy(Logs)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        global Collection
        global Logs
        message = ' -> '.join(Logs)
        if exc_val:
            Collection = False
            Logs.clear()
            Logger.output(message=message, level=self.level)
        else:
            if self.retrying:
                Logs = copy.deepcopy(self.collection)
            else:
                if self.end:
                    Collection = False
                    Logs.clear()
                    if message:
                        Logger.output(message=message, level=self.level)
