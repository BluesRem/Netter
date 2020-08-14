import re
import sys
import time
from contextlib import suppress, contextmanager

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException, \
    NoAlertPresentException

from netter.fixtures import Finder
from netter.fixtures.alert import Alert
from netter.fixtures.cookies import Cookies
from netter.fixtures.locators import *
from netter.fixtures.scroll import Scroll
from netter.fixtures.webelement.element import Element
from netter.fixtures.windows import Windows

SYSTEM_PLATFORM = {
    'win32': 'Windows',
    'linux': 'Linux',
    'darwin': 'Mac'
}[sys.platform.title()]

DRIVER_PLATFORM = {
    'iOS': 'iOS',
    'Android': 'Android'
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
        self.driver_platform = DRIVER_PLATFORM[
            driver.capabilities.get('platformName')] if driver_type == 'Appium' else SYSTEM_PLATFORM
        self.system_platform = SYSTEM_PLATFORM


class BaseWebDriver(object):
    driver = None

    def __init__(self, wait_time):
        self.wait_time = wait_time

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.quit()

    @property
    def title(self):
        return self.driver.title

    @property
    def html(self):
        return self.driver.page_source

    @property
    def url(self):
        return self.driver.current_url

    def visit(self, url, https=False):
        if '://' not in url:
            if https:
                protocol = 'https'
            else:
                protocol = 'http'
            url = f'{protocol}://{url}'
        with suppress(TimeoutException):
            self.driver.get(url=url)
            return
        self.stop()

    def stop(self):
        self.driver.execute_script('window.stop();')

    def back(self):
        self.driver.back()

    def close(self):
        self.driver.close()

    def quit(self):
        self.driver.quit()

    def forward(self):
        self.driver.forward()

    def reload(self):
        self.driver.refresh()

    def execute_script(self, script, *args):
        return self.driver.execute_script(script, *args)

    def page_timeout(self, wait_time):
        self.driver.set_page_load_timeout(time_to_wait=wait_time)

    def script_timeout(self, wait_time):
        self.driver.set_script_timeout(time_to_wait=wait_time)

    def implicitly_wait(self, wait_time):
        self.driver.implicitly_wait(time_to_wait=wait_time)

    @property
    def cookies(self):
        return Cookies(driver=self.driver)

    @property
    def windows(self):
        return Windows(driver=self.driver)

    @property
    def scroll(self):
        return Scroll(driver=self.driver)

    def is_element_visible(self, locator, wait_time=None, parent=None):
        wait_time = wait_time or self.wait_time
        end_time = time.time() + wait_time

        while time.time() < end_time:
            elements = Finder(driver=self.driver, locator=locator, parent=parent).items
            with suppress(NoSuchElementException, StaleElementReferenceException):
                for element in elements:
                    if element.is_displayed():
                        return element
        else:
            return False

    def is_element_not_visible(self, locator, wait_time=None, parent=None):
        wait_time = wait_time or self.wait_time
        end_time = time.time() + wait_time

        while time.time() < end_time:
            elements = Finder(driver=self.driver, locator=locator, parent=parent).items
            with suppress(NoSuchElementException, StaleElementReferenceException):
                for element in elements:
                    if element.is_displayed():
                        continue
                else:
                    return True
        else:
            return False

    def is_element_located(self, locator, wait_time=None, parent=None):
        wait_time = wait_time or self.wait_time
        end_time = time.time() + wait_time

        while time.time() < end_time:
            with suppress(NoSuchElementException):
                return Finder(driver=self.driver, locator=locator, parent=parent).item
        else:
            return False

    def is_element_not_located(self, locator, wait_time=None, parent=None):
        wait_time = wait_time or self.wait_time
        end_time = time.time() + wait_time

        while time.time() < end_time:
            elements = Finder(driver=self.driver, locator=locator, parent=parent).items
            if elements:
                return elements
        else:
            return False

    def is_page_loaded(self):
        return self.driver.execute_script('return document.readyState;') == 'complete'

    def is_new_window_open(self, current_windows):
        return len(current_windows) != len(self.windows)

    def is_alert_present(self):
        with suppress(NoAlertPresentException):
            alert = self.driver.switch_to.alert
            return Alert(alert=alert)
        return False

    def is_url_contains(self, url):
        return url in self.url

    def is_url_matches(self, pattern):
        return re.search(pattern, self.url)

    def is_url_to_be(self, url):
        return url == self.url

    def is_url_changes(self, url):
        return url != self.url

    def is_text_present(self, text, locator=None, wait_time=None, parent=None):
        wait_time = wait_time or self.wait_time
        locator = locator or TAG_NAME(value='body')

        elements = self.find_all(locator=locator, wait_time=wait_time, parent=parent)
        for element in elements:
            if text == element.text:
                return True
        else:
            return False

    def is_text_not_present(self, text, locator=None, wait_time=None, parent=None):
        wait_time = wait_time or self.wait_time
        locator = locator or TAG_NAME(value='body')

        elements = self.find_all(locator=locator, wait_time=wait_time, parent=parent)
        for element in elements:
            if text != element.text:
                return True
        else:
            return False

    def find(self, locator, visible=None, wait_time=None, parent=None):
        wait_time = wait_time or self.wait_time

        if element := self.is_element_visible(locator=locator, wait_time=wait_time,
                                              parent=parent) if visible else self.is_element_located(locator=locator,
                                                                                                     wait_time=wait_time,
                                                                                                     parent=parent):
            return element
        else:
            raise NoSuchElementException('Not found element.')

    def find_all(self, locator, visible=None, wait_time=None, parent=None):
        wait_time = wait_time or self.wait_time

        elements = []
        for element in self.is_element_located(locator=locator, wait_time=wait_time, parent=parent):
            if visible and element.visible:
                elements.append(element)
            elif not visible:
                elements.append(element)
        return elements

    @contextmanager
    def get_iframe(self, frame_reference: Element):
        self.driver.switch_to.frame(frame_reference=frame_reference())
        try:
            yield self
        finally:
            self.driver.switch_to.frame(frame_reference=None)

    def get_img(self, filename=None):
        if filename is None:
            filename = f'{round(time.time())}.png'
        self.driver.get_screenshot_as_file(filename=filename)
        return filename

    def get_base64(self):
        return self.driver.get_screenshot_as_base64()

    def switch_to_frame(self, frame_reference: Element):
        self.driver.switch_to.frame(frame_reference=frame_reference())

    def switch_to_default_content(self):
        self.driver.switch_to.default_content()
