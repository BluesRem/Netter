from appium.webdriver.common.mobileby import By

__all__ = ['CSS', 'XPATH', 'NAME', 'TAG_NAME', 'CLASS_NAME', 'PARTIAL_LINK_TEXT', 'LINK_TEXT', 'ID']


class Selector(object):
    def __init__(self, value, wait_time=2, describe=''):
        self._by = None
        self._value = value
        self._describe = describe
        self._wait_time = wait_time

    @property
    def locator(self):
        return self._by, self._value

    @property
    def value(self):
        return self._value

    @property
    def describe(self):
        return self._describe

    @property
    def wait_time(self):
        return self._wait_time

    def __str__(self):
        return self._describe or f'Locator:{self._by} Value:{self._value}'


class CSS(Selector):
    def __init__(self, value, wait_time=2, describe=''):
        super().__init__(value, wait_time=wait_time, describe=describe)
        self._by = By.CSS_SELECTOR


class XPATH(Selector):
    def __init__(self, value, wait_time=2, describe=''):
        super().__init__(value, wait_time=wait_time, describe=describe)
        self._by = By.XPATH


class ID(Selector):
    def __init__(self, value, wait_time=2, describe=''):
        super().__init__(value, wait_time=wait_time, describe=describe)
        self._by = By.ID


class CLASS_NAME(Selector):
    def __init__(self, value, wait_time=2, describe=''):
        super().__init__(value, wait_time=wait_time, describe=describe)
        self._by = By.CLASS_NAME


class LINK_TEXT(Selector):
    def __init__(self, value, wait_time=2, describe=''):
        super().__init__(value, wait_time=wait_time, describe=describe)
        self._by = By.LINK_TEXT


class PARTIAL_LINK_TEXT(Selector):
    def __init__(self, value, wait_time=2, describe=''):
        super().__init__(value, wait_time=wait_time, describe=describe)
        self._by = By.PARTIAL_LINK_TEXT


class NAME(Selector):
    def __init__(self, value, wait_time=2, describe=''):
        super().__init__(value, wait_time=wait_time, describe=describe)
        self._by = By.NAME


class TAG_NAME(Selector):
    def __init__(self, value, wait_time=2, describe=''):
        super().__init__(value, wait_time=wait_time, describe=describe)
        self._by = By.TAG_NAME
