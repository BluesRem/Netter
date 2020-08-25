from netter.drivers.desktop.firefox import WebDriver as FirefoxDriver
from netter.drivers.desktop.chrome import WebDriver as ChromeDriver
from netter.drivers.mobile.browser import WebDriver as AppDriver


def get_browser(name, platform, *args, **kwargs):
    if platform == 'Desktop':
        driver = {
            'Firefox': FirefoxDriver,
            'Chrome': ChromeDriver
        }[name](*args, **kwargs)
    else:
        driver = AppDriver(name, *args, **kwargs)
    return driver
