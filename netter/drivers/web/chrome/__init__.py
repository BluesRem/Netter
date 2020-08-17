from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from netter.drivers.web import BasePage
from netter.drivers.web import initial
from netter.drivers.web.chrome.options import Options


class WebDriver(BasePage):
    NAME = 'Chrome'

    def __init__(self, options_=None):
        super().__init__()
        self._options = options_ or webdriver.ChromeOptions()

    @property
    def options(self):
        return Options(options=self._options)

    @initial(name_=NAME, type_=BasePage.TYPE)
    def Local(self, executable_path="chromedriver"):
        self._driver = webdriver.Chrome(executable_path=executable_path, options=self._options)
        return self._driver

    @initial(name_=NAME, type_=BasePage.TYPE)
    def Remote(self, host='127.0.0.1', port='4444'):
        self._driver = webdriver.Remote(command_executor=f'http://{host}:{port}/wd/hub',
                                        desired_capabilities=DesiredCapabilities.CHROME,
                                        options=self._options)
        return self._driver
