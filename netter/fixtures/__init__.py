from .webelement.element import Element
from .webelement.elements import Elements


class Finder(object):
    def __init__(self, driver, locator, parent=None):
        self._driver = driver
        self._locator = locator
        self._parent = parent

    @property
    def items(self):
        parent = self._parent or self._driver
        by, value = self._locator()
        return Elements(driver=self._driver, elements=parent.find_elements(by, value), locator=self._locator)

    @property
    def item(self):
        by, value = self._locator()
        parent = self._parent or self._driver
        return Element(driver=self._driver, element=parent.find_element(by, value), locator=self._locator)

    def __call__(self, *args, **kwargs):
        return self.items
