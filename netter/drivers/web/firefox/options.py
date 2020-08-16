from selenium.webdriver import FirefoxOptions


class Options(object):
    def __init__(self, options: FirefoxOptions):
        self.options = options

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
