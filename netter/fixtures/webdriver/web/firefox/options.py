from selenium import webdriver


class Options(object):
    def __init__(self):
        self.options = webdriver.FirefoxOptions()

    @property
    def headless(self):
        return self.options.headless

    @headless.setter
    def headless(self, value: bool):
        self.options.headless = value

    def window_size(self, width, height):
        self.options.add_argument(f'-width={width}')
        self.options.add_argument(f'-height={height}')

    def add_argument(self, argument):
        self.options.add_argument(argument=argument)

    def __call__(self, *args, **kwargs):
        return self.options
