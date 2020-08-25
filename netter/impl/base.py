import time
from contextlib import suppress

from selenium.common.exceptions import StaleElementReferenceException

from selenium.common.exceptions import NoSuchElementException


class BasePage(object):
    def __init__(self, driver):
        self._driver = driver

    def _visible_element(self, selector):
        elements = self._elements(selector)
        with suppress(StaleElementReferenceException):
            for element in elements:
                if element.is_displayed():
                    return element

    def _visible_elements(self, selector):
        elements = self._elements(selector)
        with suppress(StaleElementReferenceException):
            return [element for element in elements if element.is_displayed()]

    def _element(self, selector):
        parent = getattr(self, '_element', None) or self._driver
        return parent.find_element(*selector.locator)

    def _elements(self, selector):
        parent = getattr(self, '_element', None) or self._driver
        return parent.find_elements(*selector.locator)

    def find(self, selector, visible=None, wait_time=None):
        end_time = time.time() + (wait_time or selector.wait_time)
        while True:
            element = self._visible_element(selector) if visible else self._element(selector)
            if element:
                return element
            if time.time() > end_time:
                raise NoSuchElementException('Not found element.')

    def find_all(self, selector, visible=None, wait_time=None):
        end_time = time.time() + (wait_time or selector.wait_time)
        while True:
            elements = self._visible_elements(selector) if visible else self._elements(selector)
            if elements:
                return elements
            if time.time() > end_time:
                raise NoSuchElementException('Not found elements.')
