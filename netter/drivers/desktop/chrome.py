from selenium import webdriver
from selenium.webdriver import DesiredCapabilities


class WebDriver(object):
    NAME = 'Chrome'

    def __init__(self, options=None):
        self._options = options or webdriver.ChromeOptions()

    def headless(self, value: bool):
        self._options.headless = value

    def sandbox(self, value: bool):
        arg = '--no-sandbox'
        self._options.add_argument(arg) if value else self._options.arguments.remove(arg)

    def gpu(self, value: bool):
        arg = '--disable-gpu'
        self._options.add_argument(arg) if value else self._options.arguments.remove(arg)

    def developer(self, value: bool):
        key, arg = 'excludeSwitches', 'enable-automation'
        if value:
            self._options.add_experimental_option(key, [arg, ])
        else:
            if key in self._options.experimental_options.keys():
                if arg in self._options.experimental_options.get(key):
                    self._options.experimental_options.get(key).remove(arg)

    def language(self, value: bool):
        self._options.add_argument(f'---lang={value}')

    def window_size(self, width, height):
        self._options.add_argument(f'--window-size={width},{height}')

    def emulation(self, name='Pixel 2', width=1920, height=1080):
        mobile_emulation = {"deviceName": name}
        self._options.add_experimental_option("mobileEmulation",
                                              mobile_emulation)
        self.window_size(width=width, height=height)

    @property
    def options(self):
        return self._options

    def Local(self, executable_path="chromedriver"):
        return webdriver.Chrome(executable_path=executable_path, options=self._options)

    def Remote(self, ip='127.0.0.1', port='4444'):
        return webdriver.Remote(command_executor=f'http://{ip}:{port}/wd/hub',
                                desired_capabilities=DesiredCapabilities.CHROME,
                                options=self._options)
