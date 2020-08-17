from netter.drivers import Custom


class BasePage(object):
    TYPE = 'Selenium'

    def __init__(self):
        self._driver = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._driver.quit()


def initial(type_, name_):
    def decorator(func):
        def wrapper(*args, **kwargs):
            driver = func(*args, **kwargs)
            driver.custom = Custom(driver=driver, type_=type_, name_=name_)
            return driver

        return wrapper

    return decorator
