from contextlib import contextmanager
from contextlib import suppress


class Cookies(object):
    def __init__(self, driver):
        self._driver = driver
        self._filter_attrs = None

    @property
    def all(self):
        cookies = self._driver.get_cookies()
        if self._filter_attrs:
            for cookie in cookies:
                self._filter(cookie=cookie)
        return cookies

    def get(self, name):
        cookie = self._driver.get_cookie(name=name)
        if self._filter_attrs:
            self._filter(cookie=cookie)
        return cookie

    def add(self, cookie: dict = None, cookies: list = None):
        if cookie is not None:
            self._driver.add_cookie(cookie)
        elif cookies is not None:
            for cookie in cookies:
                self._driver.add_cookie(cookie)

    def delete(self, name):
        self._driver.delete_cookie(name=name)

    def clear(self):
        self._driver.delete_all_cookies()

    def _filter(self, cookie):
        difference = set(cookie.keys()).difference(set(self._filter_attrs))
        for key in difference:
            cookie.pop(key)

    @contextmanager
    def filter(self, filter_attrs: list):
        self._filter_attrs = filter_attrs
        if 'name' not in self._filter_attrs:
            self._filter_attrs.append('name')
        with suppress(BaseException):
            yield self
        self._filter_attrs = None
