import sys

PLATFORM = {
    'iOS': 'iOS',
    'Android': 'Android',
    'win32': 'Windows',
    'linux': 'Linux',
    'darwin': 'Mac'
}


def initial(driver_type, driver_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            driver = func(*args, **kwargs)
            driver.custom = Custom(driver=driver, driver_type=driver_type, driver_name=driver_name)
            return driver

        return wrapper

    return decorator


class Custom(object):

    def __init__(self, driver, driver_type, driver_name):
        self.driver_type = driver_type
        self.driver_name = driver_name
        self.driver_platform = PLATFORM[driver.capabilities.get('platformName')]
        self.system_platform = PLATFORM[sys.platform.title()]
