import time

from netter.fixtures import logging


class Wait(object):
    def __init__(self, wait_time, ignored_exceptions=None, poll_frequency=0.5):
        self._wait_time = wait_time
        self._ignored_exceptions = ignored_exceptions if isinstance(ignored_exceptions, list) else [ignored_exceptions]
        self._poll = poll_frequency

    def until(self, method, message=''):
        end_time = time.time() + self._wait_time
        while True:
            with logging.collection() as collection:
                try:
                    result = method()
                    if result:
                        return result
                except Exception as exc:
                    if not self._ignored_exceptions or exc not in self._ignored_exceptions:
                        raise exc
                time.sleep(self._poll)
                if time.time() > end_time:
                    break
                else:
                    collection.retrying = True
        if message:
            raise TimeoutError(message)
        else:
            return False

    def until_not(self, method, message=''):
        end_time = time.time() + self._wait_time
        while True:
            with logging.collection() as collection:
                try:
                    result = method()
                    if not result:
                        return result
                except Exception as exc:
                    if not self._ignored_exceptions or exc not in self._ignored_exceptions:
                        raise exc
                time.sleep(self._poll)
                if time.time() > end_time:
                    break
                else:
                    collection.retrying = True
        if message:
            raise TimeoutError(message)
        else:
            return False
