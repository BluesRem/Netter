from appium.webdriver import Remote
from netter.drivers import Custom


class WebDriver(object):
    TYPE = 'Appium'

    def __init__(self, desired_capabilities: dict):
        self.desired_capabilities = desired_capabilities
        self._driver = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._driver.quit()

    def remote(self, host='127.0.0.1', port='4444'):
        name = self.desired_capabilities.get('browserName')
        self._driver = Remote(f'http://{host}:{port}/wd/hub', desired_capabilities=self.desired_capabilities)
        self._driver.custom = Custom(driver=self._driver, type_=self.TYPE, name_=name)
        return self._driver
