from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from netter.drivers.desktop.chrome.options import Options


class WebDriver(object):
    NAME = 'Chrome'

    def __init__(self, options=None):
        self._options = Options(options)
        self._driver = None

    def Local(self, executable_path="chromedriver"):
        self._driver = webdriver.Chrome(executable_path=executable_path, options=self._options)
        return self._driver

    def Remote(self, ip='127.0.0.1', port='4444'):
        self._driver = webdriver.Remote(command_executor=f'http://{ip}:{port}/wd/hub',
                                        desired_capabilities=DesiredCapabilities.CHROME,
                                        options=self._options)
        return self._driver
