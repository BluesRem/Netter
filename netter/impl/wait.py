import time

from netter.logging import Logger

from contextlib import suppress


class Wait(object):
    def __init__(self, wait_time, *exceptions, poll_frequency=0.5, message=''):
        self._end_time = time.time() + wait_time
        self._exceptions = exceptions
        self._poll = poll_frequency
        self._message = message

    def until(self, method, *args, **kwargs):
        Logger.debug('Wait for the result to be true')
        while True:
            with Logger() as logger:
                with suppress(*self._exceptions):
                    if method(*args, **kwargs):
                        logger.ending = True
                        return True
                logger.ending = False
                if time.time() > self._end_time:
                    logger.ending = True
                    if self._message:
                        raise AssertionError(self._message)
                    else:
                        return False

    def until_not(self, method, *args, **kwargs):
        Logger.debug('Wait for the result to be false')
        while True:
            with Logger() as logger:
                with suppress(*self._exceptions):
                    if not method(*args, **kwargs):
                        logger.ending = True
                        return True
                logger.ending = False
                if time.time() > self._end_time:
                    logger.ending = True
                    if self._message:
                        raise AssertionError(self._message)
                    else:
                        return False
