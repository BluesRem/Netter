class Windows(object):
    def __init__(self, driver):
        self._driver = driver

    @property
    def current(self):
        return self._driver.current_window_handle

    @property
    def items(self):
        return self._driver.window_handles

    @property
    def first(self):
        return self.items[0]

    @property
    def last(self):
        return self.items[-1]

    def switch(self, index):
        self._driver.switch_to.window(window_name=self.items[index])

    def switch_new_window(self, before_windows):
        new_window = set(self.items).difference(set(before_windows)).pop()
        self._driver.switch_to.window(window_name=new_window)

    def __len__(self):
        return len(self.items)

    def __getitem__(self, key):
        return self.items[key]
