from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from netter.drivers.web import BasePage
from netter.drivers.web import initial
from netter.drivers.web.firefox.options import Options
from netter.drivers.web.firefox.profile import Profile


class WebDriver(BasePage):
    NAME = 'Firefox'

    def __init__(self, options_=None, profile_=None):
        super().__init__()
        self._options = options_ or webdriver.FirefoxOptions()
        self._profile = profile_ or webdriver.FirefoxProfile()

    @property
    def options(self):
        return Options(options=self._options)

    @property
    def profile(self):
        return Profile(profile=self._profile)

    @initial(name_=NAME, type_=BasePage.TYPE)
    def Local(self, executable_path="chromedriver"):
        self._driver = webdriver.Firefox(executable_path=executable_path, options=self._options,
                                         firefox_profile=self._profile)
        return self._driver

    @initial(name_=NAME, type_=BasePage.TYPE)
    def Remote(self, host='127.0.0.1', port='4444'):
        self._driver = webdriver.Remote(command_executor=f'http://{host}:{port}/wd/hub',
                                        desired_capabilities=DesiredCapabilities.FIREFOX,
                                        options=self._options, browser_profile=self._profile)
        return self._driver
