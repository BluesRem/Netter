from selenium.webdriver import Chrome, DesiredCapabilities
from selenium.webdriver import Remote

from netter.fixtures.drivers import initial
from netter.fixtures.drivers.web import BasePage
from netter.fixtures.drivers.web.chrome.options import Options


class WebDriver(BasePage):
    driver_name = "Chrome"

    def __init__(self, wait_time=2):
        super().__init__(wait_time=wait_time)
        self._options = Options()

    @property
    def options(self):
        return self._options

    @initial(driver_type=BasePage.driver_type, driver_name=driver_name)
    def local(self, executable_path="chromedriver"):
        self.driver = Chrome(executable_path=executable_path, options=self.options())
        return self.driver

    @initial(driver_type=BasePage.driver_type, driver_name=driver_name)
    def remote(self, host='127.0.0.1', port='4444'):
        self.driver = Remote(command_executor=f'http://{host}:{port}/wd/hub',
                             desired_capabilities=DesiredCapabilities.CHROME,
                             options=self.options())
        return self.driver
