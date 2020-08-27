from typing import ClassVar

BROWSER = {
    'CHROME': 'Chrome',
    'FIREFOX': 'Firefox'
}

OS = {
    'iOS': 'iOS',
    'Android': 'Android',
    'win32': 'Windows',
    'linux': 'Linux',
    'darwin': 'Mac'
}

PLATFORM = {
    'DESKTOP': 'Desktop',
    "MOBILE": 'Mobile'
}


class GetBrowser(object):
    def __init__(self, name: str, platform: str):
        self._name = BROWSER[name.upper()]
        self._platform = PLATFORM[platform.upper()]

    @property
    def _driver(self):
        if self._platform == 'Desktop':
            from selenium import webdriver
            return webdriver
        else:
            from appium import webdriver
            return webdriver

    def _initialize(self, driver):
        setattr(driver, 'attr', ClassVar)
        setattr(driver.attr, 'name', self._name)
        setattr(driver.attr, 'type', 'Selenium' if self._platform == 'Desktop' else 'Appium')
        setattr(driver.attr, 'os', OS[driver.capabilities.get('platformName')])
        return driver

    def local(self, *args, **kwargs):
        if self._platform == 'Desktop':
            if self._name == 'Chrome':
                driver = self._driver.Chrome(*args, **kwargs)
            elif self._name == 'Firefox':
                driver = self._driver.Firefox(*args, **kwargs)
            else:
                raise NameError(f'No found {self._name}')
        else:
            driver = self._driver.Remote(*args, **kwargs)
        return self._initialize(driver)

    def remote(self, ip, port, *args, **kwargs):
        command_executor = f'http://{ip}:{port}/wd/hub'
        if self._platform == 'Desktop':
            from selenium.webdriver import DesiredCapabilities
            desired_capabilities = {
                'Chrome': DesiredCapabilities.CHROME,
                'Firefox': DesiredCapabilities.CHROME,
            }[self._name]
            driver = self._driver.Remote(command_executor=command_executor, desired_capabilities=desired_capabilities,
                                         *args,
                                         **kwargs)
        else:
            driver = self._driver.Remote(command_executor=command_executor, *args, **kwargs)
        return self._initialize(driver)
