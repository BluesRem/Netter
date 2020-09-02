import time
from contextlib import suppress

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

from src.netter.logging import Logger


class BasePage(object):
    def __init__(self, driver):
        self._driver = driver

    def _get_element(self, selector):
        with suppress(NoSuchElementException):
            parent = getattr(self, '_element', None) or self._driver
            return parent.find_element(*selector.locator)

    def _get_elements(self, selector):
        parent = getattr(self, '_element', None) or self._driver
        return parent.find_elements(*selector.locator)

    def _visible_element(self, selector):
        elements = self._get_elements(selector)
        for element in elements:
            with suppress(StaleElementReferenceException):
                if element.is_displayed():
                    return element

    def _visible_elements(self, selector):
        elements = self._get_elements(selector)
        with suppress(StaleElementReferenceException):
            return [element for element in elements if element.is_displayed()]

    def _find(self, selector, visible=None, wait_time=None):
        end_time = time.time() + (wait_time or selector.wait_time)
        while True:
            element = self._visible_element(selector) if visible else self._get_element(selector)
            if element:
                return element
            if time.time() > end_time:
                raise NoSuchElementException(f'找不到元素：{selector}')

    def _find_all(self, selector, visible=None, wait_time=None):
        end_time = time.time() + (wait_time or selector.wait_time)
        while True:
            elements = self._visible_elements(selector) if visible else self._get_elements(selector)
            if elements:
                return elements
            if time.time() > end_time:
                raise NoSuchElementException(f'找不到元素：{selector}')

    def assert_element_visible(self, selector):
        class Wrapper:
            outer_class = self

            def __init__(self, *args):
                self._selector, *_ = args

            def __call__(self, *args, **kwargs):
                if self.outer_class._visible_element(self._selector):
                    return True
                else:
                    return False

        return Wrapper(selector)

    def assert_element_located(self, selector):
        class Wrapper:
            outer_class = self

            def __init__(self, *args):
                self._selector, *_ = args

            def __call__(self, *args, **kwargs):
                if self.outer_class._get_element(self._selector):
                    return True
                else:
                    return False

        return Wrapper(selector)

    def assert_text_is(self, text, selector):
        class Wrapper:
            outer_class = self

            def __init__(self, *args):
                self._text, self._selector = args

            def __call__(self, *args, **kwargs):
                _text = self.outer_class._get_element(self._selector).text
                Logger.debug(f'判断元素{self._selector}的文本是否包含：{text}，当前文本为：{_text}')
                return self._text == _text

        return Wrapper(text, selector)

    def assert_attr_is(self, name, value, selector):
        class Wrapper:
            outer_class = self

            def __init__(self, *args):
                self._name, self._value, self._selector = args

            def __call__(self, *args, **kwargs):
                _value = self.outer_class._get_element(self._selector).get_attribute(name)
                Logger.debug(f'判断元素{self._selector}的属性{name}是否包含：{value}，当前值为：{_value}')
                return self._value == _value

        return Wrapper(name, value, selector)
