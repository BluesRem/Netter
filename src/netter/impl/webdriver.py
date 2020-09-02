import re
import time
from contextlib import contextmanager
from contextlib import suppress
from typing import Tuple

from selenium.common.exceptions import NoAlertPresentException

from src.netter.impl.base import BasePage
from src.netter.impl.cookies import Cookies
from src.netter.impl.element import Element, Elements
from src.netter.impl.scroll import Scroll
from src.netter.impl.wait import Wait
from src.netter.impl.windows import Windows
from src.netter.logging import Logger


class WebDriver(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self._page_timeout = None

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
            Logger.debug(f'自动添加{protocol}协议')
        Logger.debug(f'加载链接：{url}')
        self._driver.get(url)

    def stop(self):
        Logger.debug('停止页面加载')
        self._driver.execute_script('window.stop();')

    def back(self):
        with self.wait_for_page_load():
            Logger.debug('回返上一页')
            self._driver.back()

    def close(self):
        Logger.debug('关闭标签页')
        self._driver.close()

    def quit(self):
        Logger.debug('退出浏览器')
        self._driver.quit()

    def forward(self):
        with self.wait_for_page_load():
            Logger.debug('前往下一页')
            self._driver.forward()

    def refresh(self):
        with self.wait_for_page_load():
            Logger.debug('刷新页面')
            self._driver.refresh()

    @staticmethod
    def wait(sec=1):
        time.sleep(sec)

    def execute_script(self, script, *args):
        return self._driver.execute_script(script, *args)

    @property
    def title(self):
        title = self._driver.title
        Logger.debug(f'当前标题为：{title}')
        return title

    @property
    def html(self):
        return self._driver.page_source

    @property
    def url(self):
        url = self._driver.current_url
        Logger.debug(f'当前链接为：{url}')
        return url

    @property
    def size(self):
        width, height = self._driver.get_window_size().values()
        Logger.debug(f'当前窗口大小为：{width} {height}')
        return {"width": width, "height": height}

    def page_timeout(self, wait_time):
        self._page_timeout = wait_time
        Logger.debug(f'设置页面加载超时时间：{wait_time}秒')
        self._driver.set_page_load_timeout(time_to_wait=wait_time)

    def script_timeout(self, wait_time):
        Logger.debug(f'设置脚本超时时间：{wait_time}秒')
        self._driver.set_script_timeout(time_to_wait=wait_time)

    def implicitly_wait(self, wait_time):
        Logger.debug(f'设置隐性时间：{wait_time}秒')
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
            Logger.debug(f'设置窗口大小为：{width} {height}')
            self._driver.set_window_size(width=width, height=height)

    def maximize(self):
        if self._driver.attr.type == 'Selenium':
            Logger.debug('窗口最大化')
            self._driver.maximize_window()

    def minimize(self):
        if self._driver.attr.type == 'Selenium':
            Logger.debug('窗口最小化')
            self._driver.minimize_window()

    def get_img(self, filename=None):
        if filename is None:
            filename = f'{round(time.time())}.png'
        Logger.debug(f'截图并保存到：{filename}')
        self._driver.get_screenshot_as_file(filename=filename)
        return filename

    def get_base64(self):
        Logger.debug('截图并保存为Base64格式')
        return self._driver.get_screenshot_as_base64()

    def assert_page_loaded(self):
        class Wrapper:
            outer_class = self

            def __call__(self, *args, **kwargs):
                Logger.debug('判断页面是否加载完毕')
                return self.outer_class.execute_script('return document.readyState;') == 'complete'

        return Wrapper()

    def assert_new_window_open(self, current_windows):
        class Wrapper:
            outer_class = self

            def __init__(self, *args):
                self._current_windows, *_ = args

            def __call__(self, *args, **kwargs):
                Logger.debug('判断是否有新窗口打开')
                return len(self._current_windows) != len(self.outer_class.windows)

        return Wrapper(current_windows)

    def assert_alert_present(self):
        class Wrapper:
            outer_class = self

            def __call__(self, *args, **kwargs):
                Logger.debug('判断弹窗是否显示')
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
                Logger.debug(f'判断链接是否包含：{url}')
                return self._url in self.outer_class.url

        return Wrapper(url)

    def assert_url_matches(self, pattern):
        class Wrapper:
            outer_class = self

            def __init__(self, *args):
                self._pattern, *_ = args

            def __call__(self, *args, **kwargs):
                Logger.debug(f'判断链接是否满足正则规则：{pattern}')
                return re.search(self._pattern, self.outer_class.url)

        return Wrapper(pattern)

    def assert_url_is(self, url):
        class Wrapper:
            outer_class = self

            def __init__(self, *args):
                self._url, *_ = args

            def __call__(self, *args, **kwargs):
                Logger.debug(f'判断链接是否等于：{url}')
                return self._url == self.outer_class.url

        return Wrapper(url)

    def assert_url_changes(self, url):
        class Wrapper:
            outer_class = self

            def __init__(self, *args):
                self._url, *_ = args

            def __call__(self, *args, **kwargs):
                Logger.debug(f'判断链接是否不等于：{url}')
                return self._url != self.outer_class.url

        return Wrapper(url)

    @contextmanager
    def wait_for_page_load(self, wait_time=15):
        wait_time = self._page_timeout or wait_time
        yield
        if not Wait(wait_time).until(self.assert_page_loaded()):
            self.stop()

    def find(self, selector, visible=None, wait_time=None):
        element = self._find(selector, visible, wait_time)
        return Element(self._driver, element, selector)

    def find_all(self, selector, visible=None, wait_time=None):
        elements = self._find_all(selector, visible, wait_time)
        return Elements(self._driver, elements, selector)
