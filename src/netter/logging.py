import os
import sys

from loguru import logger

LEVEL = {
    'TRACE', 5,
    'DEBUG', 10,
    'INFO', 20,
    'SUCCESS', 25,
    'WARNING', 30,
    'ERROR', 40,
    'CRITICAL', 50
}


def initial(level='DEBUG', logfile=None, stdout=True):
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


class Logger(object):
    _messages = None

    def __init__(self, level='DEBUG'):
        self._level = level
        self.ending = True

    def __enter__(self):
        Logger._messages = []
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.ending:
            if self._messages:
                logger.log(self._level, ' -> '.join(self._messages))
            if exc_val:
                logger.error(exc_val)
        Logger._messages = None

    @classmethod
    def trace(cls, message, *args, **kwargs):
        cls._log('TRACE', message, *args, **kwargs)

    @classmethod
    def debug(cls, message, *args, **kwargs):
        cls._log('DEBUG', message, *args, **kwargs)

    @classmethod
    def info(cls, message, *args, **kwargs):
        cls._log('INFO', message, *args, **kwargs)

    @classmethod
    def success(cls, message, *args, **kwargs):
        cls._log('SUCCESS', message, *args, **kwargs)

    @classmethod
    def warning(cls, message, *args, **kwargs):
        cls._log('WARNING', message, *args, **kwargs)

    @classmethod
    def error(cls, message, *args, **kwargs):
        cls._log('ERROR', message, *args, **kwargs)

    @classmethod
    def critical(cls, message, *args, **kwargs):
        cls._log('CRITICAL', message, *args, **kwargs)

    @classmethod
    def _log(cls, level, message, *args, **kwargs):
        if cls._messages is None:
            logger.log(level, message, *args, **kwargs)
        else:
            cls._messages.append(message.format(*args, **kwargs))
