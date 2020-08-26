import random
import time
from contextlib import contextmanager, suppress

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

from netter.impl.base import BasePage


class Element(BasePage):
    def __init__(self, driver, element, selector):
        super().__init__(driver)
        self._element = element
        self._selector = selector

    @property
    def visible(self):
        return self._element.is_displayed()

    @property
    def enabled(self):
        return self._element.is_enabled()

    @property
    def size(self):
        return self._element.size.values()

    @property
    def text(self):
        return self._element.text

    def attr(self, name):
        return self._element.get_attribute(name=name)

    @property
    def view_position(self) -> dict:
        return self._driver.execute_script("""
        //计算x坐标
        var actualLeft = arguments[0].offsetLeft;
        var current = arguments[0].offsetParent;
        while (current !== null) {
            actualLeft += (current.offsetLeft + current.clientLeft);
            current = current.offsetParent;
        }
        if (document.compatMode == "BackCompat") {
            var elementScrollLeft = document.body.scrollLeft;
        } else {
            var elementScrollLeft = document.documentElement.scrollLeft;
        }
        var left = actualLeft - elementScrollLeft;
        //计算y坐标
        var actualTop = arguments[0].offsetTop;
        var current = arguments[0].offsetParent;
        while (current !== null) {
            actualTop += (current.offsetTop + current.clientTop);
            current = current.offsetParent;
        }
        if (document.compatMode == "BackCompat") {
            var elementScrollTop = document.body.scrollTop;
        } else {
            var elementScrollTop = document.documentElement.scrollTop;
        }
        var right = actualTop - elementScrollTop;
        //返回结果
        return {
            x: left,
            y: right
        }
        """, self._element)

    @property
    def page_position(self) -> dict:
        return self._driver.execute_script("""
        //计算x坐标
        var actualLeft = arguments[0].offsetLeft;
        var current = arguments[0].offsetParent;
        while (current !== null) {
            actualLeft += current.offsetLeft;
            current = current.offsetParent;
        }
        //计算y坐标
        var actualTop = arguments[0].offsetTop;
        var current = arguments[0].offsetParent;
        while (current !== null) {
            actualTop += (current.offsetTop + current.clientTop);
            current = current.offsetParent;
        }
        //返回结果
        return {
            x: actualLeft,
            y: actualTop
        }
        """, self._element)

    @property
    def in_view(self):
        in_view = self._driver.execute_script("""
        var rect = arguments[0].getBoundingClientRect();
        var windowHeight = (window.innerHeight || document.documentElement.clientHeight);
        var windowWidth = (window.innerWidth || document.documentElement.clientWidth);        
        var vertInView = (rect.top <= windowHeight) && ((rect.top + rect.height) >= 0);
        var horInView = (rect.left <= windowWidth) && ((rect.left + rect.width) >= 0);        
        return (vertInView && horInView);
        """, self._element)
        return True if in_view else False

    def highlight(self, clear=True):
        previous_style = self.attr('style')
        self._driver.execute_script('arguments[0].setAttribute("style", "border: 2px solid red; font-weight: bold;");',
                                    self._element)
        if clear:
            time.sleep(0.5)
            if previous_style:
                self._driver.execute_script(
                    f'arguments[0].setAttribute("style", "{previous_style}");', self._element)
            else:
                self._driver.execute_script('arguments[0].removeAttribute("style");', self._element)

    def scroll_into_view(self, stay=0.5):
        self._driver.execute_script('arguments[0].scrollIntoView({block: "center"});', self._element)
        time.sleep(stay)

    @contextmanager
    def action_native_tap(self):
        if self._driver.attr.type == 'Appium':
            self._driver.update_settings({'nativeWebTap': True})
            with suppress(BaseException):
                yield
            self._driver.update_settings({'nativeWebTap': False})
        else:
            yield

    def click(self, native_tap=None, stay=0.5):
        if not self.in_view:
            self.scroll_into_view(stay=stay)
        self.highlight()
        if self._driver.attr.type == 'Selenium':
            if self._driver.attr.name in ['IE', 'Safari']:
                self._driver.execute_script('arguments[0].click();', self._element)
                return
        elif self._driver.attr.type == 'Appium' and self._driver.attr.name == 'Safari':
            if native_tap:
                with self.action_native_tap():
                    self._element.click()
                return
        self._element.click()

    def input(self, value, clear=True, stay=0.5):
        if not self.in_view:
            self.scroll_into_view(stay=stay)
        self.highlight()
        if clear:
            self._driver.execute_script('arguments[0].select();', self._element)
            self._element.send_keys(Keys.DELETE)
            time.sleep(0.5)
        self._element.send_keys(value)

    def select_by_index(self, index):
        if not self.in_view:
            self.scroll_into_view()
        self.highlight()
        Select(webelement=self._element).select_by_index(index=index)

    def select_by_value(self, value):
        if not self.in_view:
            self.scroll_into_view()
        self.highlight()
        Select(webelement=self._element).select_by_value(value=value)

    def select_by_text(self, text):
        if not self.in_view:
            self.scroll_into_view()
        self.highlight()
        Select(webelement=self._element).select_by_visible_text(text=text)

    def find(self, selector, visible=None, wait_time=None):
        element = self._find(selector, visible, wait_time)
        return Element(self._driver, element, self._selector)

    def find_all(self, selector, visible=None, wait_time=None):
        elements = self._find_all(selector, visible, wait_time)
        return Elements(self._driver, elements, self._selector)


class Elements(BasePage):
    def __init__(self, driver, elements, selector):
        super().__init__(driver)
        self._elements = elements
        self._selector = selector

    @property
    def items(self):
        return [Element(self._driver, element, self._selector) for element in self._elements]

    @property
    def first(self):
        return self.items[0]

    @property
    def last(self):
        return self.items[-1]

    @property
    def random(self):
        return random.choice(self.items)

    def __getitem__(self, index):
        return self.items[index]

    def __len__(self):
        return len(self._elements)
