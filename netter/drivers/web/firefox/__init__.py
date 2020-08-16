from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from netter.drivers.web.firefox.options import Options
from netter.drivers.web.firefox.profile import Profile


class WebDriver(object):

    def __init__(self, options_=None, profile_=None):
        self._options = options_ or webdriver.FirefoxOptions()
        self._profile = profile_ or webdriver.FirefoxProfile()

    @property
    def options(self):
        return Options(options=self._options)

    @property
    def profile(self):
        return Profile(profile=self._profile)

    def Local(self, executable_path="chromedriver"):
        return webdriver.Firefox(executable_path=executable_path, options=self._options, firefox_profile=self._profile)

    def Remote(self, host='127.0.0.1', port='4444'):
        return webdriver.Remote(command_executor=f'http://{host}:{port}/wd/hub',
                                desired_capabilities=DesiredCapabilities.FIREFOX,
                                options=self._options, browser_profile=self._profile)
