from typing import Tuple


class Windows(object):
    def __init__(self, driver):
        self._driver = driver

    @property
    def current(self):
        return self._driver.current_window_handle

    @property
    def all(self):
        return self._driver.window_handles

    @property
    def first(self):
        return self.all[0]

    @property
    def last(self):
        return self.all[-1]

    @property
    def size(self):
        width, height = self._driver.get_window_size().values()
        return {"width": width, "height": height}

    @size.setter
    def size(self, value: Tuple[float, float]):
        if self._driver.type == 'Selenium':
            width, height = value
            self._driver.set_window_size(width=width, height=height)

    def maximize(self):
        if self._driver.type == 'Selenium':
            self._driver.maximize_window()

    def minimize(self):
        if self._driver.type == 'Selenium':
            self._driver.minimize_window()

    def switch(self, index):
        self._driver.switch_to.window(window_name=self.all[index])

    def switch_new_window(self, before_windows):
        new_window = set(self.all).difference(set(before_windows)).pop()
        self._driver.switch_to.window(window_name=new_window)

    def __len__(self):
        return len(self.all)

    def __getitem__(self, key):
        return self.all[key]


if __name__ == '__main__':
    a = Windows([1, 2, 3, 4])
    print(len(a))
