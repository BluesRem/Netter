import re
import time
from contextlib import suppress
from typing import Tuple

from selenium.common.exceptions import TimeoutException, NoAlertPresentException

from netter.impl.base import BasePage
from netter.impl.cookies import Cookies
from netter.impl.element import Element, Elements
from netter.impl.scroll import Scroll
from netter.impl.windows import Windows
from netter.impl.wait import Wait


class WebDriver(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.quit()

    def get(self, url, https=False):
        if '://' not in url:
            if https:
                protocol = 'https'
            else:
                protocol = 'http'
            url = f'{protocol}://{url}'
        with suppress(TimeoutException):
            self._driver.get(url)
            return
        self.stop()

    def stop(self):
        self._driver.execute_script('window.stop();')

    def back(self):
        self._driver.back()

    def close(self):
        self._driver.close()

    def quit(self):
        self._driver.quit()

    def forward(self):
        self._driver.forward()

    def reload(self):
        self._driver.refresh()

    def waiting_for_load(self, wait_time=15):
        if not Wait(wait_time).until(self.assert_page_loaded()):
            self.stop()

    @staticmethod
    def wait(sec=1):
        time.sleep(sec)

    def execute_script(self, script, *args):
        return self._driver.execute_script(script, *args)

    @property
    def title(self):
        return self._driver.title

    @property
    def html(self):
        return self._driver.page_source

    @property
    def url(self):
        return self._driver.current_url

    @property
    def size(self):
        width, height = self._driver.get_window_size().values()
        return {"width": width, "height": height}

    def page_timeout(self, wait_time):
        self._driver.set_page_load_timeout(time_to_wait=wait_time)

    def script_timeout(self, wait_time):
        self._driver.set_script_timeout(time_to_wait=wait_time)

    def implicitly_wait(self, wait_time):
        self._driver.implicitly_wait(time_to_wait=wait_time)

    @property
    def cookies(self):
        return Cookies(driver=self._driver)

    @property
    def windows(self):
        return Windows(driver=self._driver)

    @property
    def scroll(self):
        return Scroll(driver=self._driver)

    @size.setter
    def size(self, value: Tuple[float, float]):
        if self._driver.attr.type == 'Selenium':
            width, height = value
            self._driver.set_window_size(width=width, height=height)

    def maximize(self):
        if self._driver.attr.type == 'Selenium':
            self._driver.maximize_window()

    def minimize(self):
        if self._driver.attr.type == 'Selenium':
            self._driver.minimize_window()

    def get_img(self, filename=None):
        if filename is None:
            filename = f'{round(time.time())}.png'
        self._driver.get_screenshot_as_file(filename=filename)
        return filename

    def get_base64(self):
        return self._driver.get_screenshot_as_base64()

    def assert_page_loaded(self):
        class Wrapper:
            outer_class = self

            def __call__(self, *args, **kwargs):
                return self.outer_class.execute_script('return document.readyState;') == 'complete'

        return Wrapper()

    def assert_new_window_open(self, current_windows):
        class Wrapper:
            outer_class = self

            def __init__(self, *args):
                self._current_windows, *_ = args

            def __call__(self, *args, **kwargs):
                return len(self._current_windows) != len(self.outer_class.windows)

        return Wrapper(current_windows)

    def assert_alert_present(self):
        class Wrapper:
            outer_class = self

            def __call__(self, *args, **kwargs):
                with suppress(NoAlertPresentException):
                    alert = self.outer_class._driver.switch_to.alert
                    return alert
                return False

        return Wrapper()

    def assert_url_contains(self, url):
        class Wrapper:
            outer_class = self

            def __init__(self, *args):
                self._url, *_ = args

            def __call__(self, *args, **kwargs):
                return self._url in self.outer_class.url

        return Wrapper(url)

    def assert_url_matches(self, pattern):
        class Wrapper:
            outer_class = self

            def __init__(self, *args):
                self._pattern, *_ = args

            def __call__(self, *args, **kwargs):
                return re.search(self._pattern, self.outer_class.url)

        return Wrapper(pattern)

    def assert_url_is(self, url):
        class Wrapper:
            outer_class = self

            def __init__(self, *args):
                self._url, *_ = args

            def __call__(self, *args, **kwargs):
                return self._url == self.outer_class.url

        return Wrapper(url)

    def assert_url_changes(self, url):
        class Wrapper:
            outer_class = self

            def __init__(self, *args):
                self._url, *_ = args

            def __call__(self, *args, **kwargs):
                return self._url != self.outer_class.url

        return Wrapper(url)

    def find(self, selector, visible=None, wait_time=None):
        element = self._find(selector, visible, wait_time)
        return Element(self._driver, element, selector)

    def find_all(self, selector, visible=None, wait_time=None):
        elements = self._find_all(selector, visible, wait_time)
        return Elements(self._driver, elements, selector)
