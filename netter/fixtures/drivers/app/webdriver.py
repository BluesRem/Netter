from appium.webdriver import Remote

from netter.fixtures.drivers import initial
from netter.fixtures.drivers.app import BasePage

driver_name = None


class WebDriver(BasePage):

    def __init__(self, desired_capabilities: dict, wait_time=2):
        super().__init__(wait_time)
        global driver_name
        driver_name = desired_capabilities['browserName']
        self.desired_capabilities = desired_capabilities

    @initial(driver_type=BasePage.driver_type, driver_name=driver_name)
    def remote(self, host='127.0.0.1', port='4444'):
        self.driver = Remote(f'http://{host}:{port}/wd/hub', desired_capabilities=self.desired_capabilities)
        return self.driver
