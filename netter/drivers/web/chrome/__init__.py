from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from netter.drivers.web.chrome.options import Options
from netter.drivers.web import BasePage
from netter.drivers import initial


class WebDriver(BasePage):
    NAME = 'Chrome'

    def __init__(self, options_=None):
        self._options = options_ or webdriver.ChromeOptions()

    @property
    def options(self):
        return Options(options=self._options)

    @initial(driver_name=NAME, driver_type=BasePage.PLATFORM)
    def Local(self, executable_path="chromedriver"):
        return webdriver.Chrome(executable_path=executable_path, options=self._options)

    @initial(driver_name=NAME, driver_type=BasePage.PLATFORM)
    def Remote(self, host='127.0.0.1', port='4444'):
        return webdriver.Remote(command_executor=f'http://{host}:{port}/wd/hub',
                                desired_capabilities=DesiredCapabilities.CHROME,
                                options=self._options)
