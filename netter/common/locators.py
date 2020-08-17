from appium.webdriver.common.mobileby import By

__all__ = ['CSS', 'XPATH', 'NAME', 'TAG_NAME', 'CLASS_NAME', 'PARTIAL_LINK_TEXT', 'LINK_TEXT', 'ID']


class Locator(object):
    def __init__(self, value, timeout=2, describe=''):
        self._value = value
        self._describe = describe
        self._timeout = timeout
        self._by = None

    @property
    def describe(self):
        return self._describe

    @property
    def timeout(self):
        return self._timeout

    def __call__(self, *args, **kwargs):
        return self._by, self._value

    def __str__(self):
        return self._describe or f'({self._by}, {self._value})'


class CSS(Locator):
    def __init__(self, value, timeout=2, describe=''):
        super().__init__(value, timeout=timeout, describe=describe)
        self._by = By.CSS_SELECTOR


class XPATH(Locator):
    def __init__(self, value, timeout=2, describe=''):
        super().__init__(value, timeout=timeout, describe=describe)
        self._by = By.XPATH


class ID(Locator):
    def __init__(self, value, timeout=2, describe=''):
        super().__init__(value, timeout=timeout, describe=describe)
        self._by = By.ID


class CLASS_NAME(Locator):
    def __init__(self, value, timeout=2, describe=''):
        super().__init__(value, timeout=timeout, describe=describe)
        self._by = By.CLASS_NAME


class LINK_TEXT(Locator):
    def __init__(self, value, timeout=2, describe=''):
        super().__init__(value, timeout=timeout, describe=describe)
        self._by = By.LINK_TEXT


class PARTIAL_LINK_TEXT(Locator):
    def __init__(self, value, timeout=2, describe=''):
        super().__init__(value, timeout=timeout, describe=describe)
        self._by = By.PARTIAL_LINK_TEXT


class NAME(Locator):
    def __init__(self, value, timeout=2, describe=''):
        super().__init__(value, timeout=timeout, describe=describe)
        self._by = By.NAME


class TAG_NAME(Locator):
    def __init__(self, value, timeout=2, describe=''):
        super().__init__(value, timeout=timeout, describe=describe)
        self._by = By.TAG_NAME
