from typing import Tuple


class Scroll(object):
    def __init__(self, driver):
        self._driver = driver

    def to_position(self, position: Tuple[float, float]):
        self._driver.execute_script('window.scrollTo({top:arguments[0], left:arguments[1]});', *position)

    def by_offset(self, offset: Tuple[float, float]):
        self._driver.execute_script('window.scrollBy(arguments[0], arguments[1]);', *offset)

    def down(self, offset=100):
        self.by_offset((0, offset))

    def up(self, offset=100):
        self.by_offset((0, -offset))

    def right(self, offset=100):
        self.by_offset((offset, 0))

    def left(self, offset=100):
        self.by_offset((-offset, 0))

    def page_up(self):
        self.by_offset((0, self._driver.execute_script('return -window.innerHeight')))

    def page_down(self):
        self.by_offset((0, -self._driver.execute_script('return -window.innerHeight')))
