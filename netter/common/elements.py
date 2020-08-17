import random

from netter.common.element import Element


class Elements(object):
    def __init__(self, driver, elements, locator):
        self.driver = driver
        self.elements = elements
        self._locator = locator

    def __len__(self):
        return len(self.all)

    def __getitem__(self, key):
        return self.all[key]

    def __str__(self):
        return self._locator

    @property
    def all(self):
        return [Element(driver=self.driver, element=element, locator=self._locator) for element in self.elements]

    @property
    def first(self):
        return self.all[0]

    @property
    def last(self):
        return self.all[-1]

    @property
    def random(self):
        return random.choice(self.all)
