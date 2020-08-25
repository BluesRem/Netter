from selenium import webdriver
from selenium.webdriver import DesiredCapabilities


class WebDriver(object):
    NAME = 'Firefox'

    def __init__(self, options=None, profile_directory=None):
        self._options = options or webdriver.FirefoxOptions()
        self._profile = webdriver.FirefoxProfile(profile_directory)

    def headless(self, value: bool):
        self._options.headless = value

    def window_size(self, width, height):
        self._options.add_argument(f'-width={width}')
        self._options.add_argument(f'-height={height}')

    @property
    def options(self):
        return self._options

    @property
    def profile(self):
        return self._profile

    def Local(self, executable_path="geckodriver"):
        return webdriver.Firefox(executable_path=executable_path,
                                 options=self._options,
                                 firefox_profile=self._profile)

    def Remote(self, ip='127.0.0.1', port='4444'):
        return webdriver.Remote(
            command_executor=f'http://{ip}:{port}/wd/hub',
            desired_capabilities=DesiredCapabilities.FIREFOX,
            options=self._options, browser_profile=self._profile)
