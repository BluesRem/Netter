from selenium.webdriver import Firefox, DesiredCapabilities
from selenium.webdriver import Remote

from netter.fixtures.drivers import initial
from netter.fixtures.drivers.web import BasePage
from netter.fixtures.drivers.web.firefox.options import Options
from netter.fixtures.drivers.web.firefox.profile import Profile


class WebDriver(BasePage):
    driver_name = "Firefox"

    def __init__(self, profile_directory=None, wait_time=2):
        super().__init__(wait_time=wait_time)
        self._options = Options()
        self._profile = Profile(profile_directory=profile_directory)

    @property
    def options(self):
        return self._options

    @property
    def profile(self):
        return self._profile

    @initial(driver_type=BasePage.driver_type, driver_name=driver_name)
    def local(self, executable_path="geckodriver"):
        self.driver = Firefox(executable_path=executable_path, options=self.options(),
                              firefox_profile=self.profile())
        return self.driver

    @initial(driver_type=BasePage.driver_type, driver_name=driver_name)
    def remote(self, host='127.0.0.1', port='4444'):
        self.driver = Remote(command_executor=f'http://{host}:{port}/wd/hub',
                             desired_capabilities=DesiredCapabilities.FIREFOX,
                             options=self.options(), browser_profile=self.profile())
        return self.driver
