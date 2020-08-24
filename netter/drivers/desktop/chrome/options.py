from selenium.webdriver import ChromeOptions


class Options(object):
    def __init__(self, options: ChromeOptions = None):
        self.options = options or ChromeOptions()

    @property
    def headless(self):
        return '--headless' in self.options.arguments

    @headless.setter
    def headless(self, value: bool):
        self.options.headless = value

    @property
    def sandbox(self):
        return '--no-sandbox' in self.options.arguments

    @sandbox.setter
    def sandbox(self, value: bool):
        arg = '--no-sandbox'
        self.options.add_argument(arg) if value else self.options.arguments.remove(arg)

    @property
    def gpu(self):
        return '--disable-gpu' in self.options.arguments

    @gpu.setter
    def gpu(self, value: bool):
        arg = '--disable-gpu'
        self.options.add_argument(arg) if value else self.options.arguments.remove(arg)

    @property
    def developer(self):
        if 'excludeSwitches' in self.options.experimental_options.keys():
            return 'enable-automation' in self.options.experimental_options.get('excludeSwitches')
        return False

    @developer.setter
    def developer(self, value: bool):
        key, arg = 'excludeSwitches', 'enable-automation'
        if value:
            self.options.add_experimental_option(key, [arg, ])
        else:
            if key in self.options.experimental_options.keys():
                if arg in self.options.experimental_options.get(key):
                    self.options.experimental_options.get(key).remove(arg)

    def language(self, value: bool):
        self.options.add_argument(f'---lang={value}')

    def window_size(self, width, height):
        self.options.add_argument(f'--window-size={width},{height}')

    def emulation(self, name='Pixel 2', width=1920, height=1080):
        mobile_emulation = {"deviceName": name}
        self.options.add_experimental_option("mobileEmulation",
                                             mobile_emulation)
        self.window_size(width=width, height=height)

    def add_argument(self, argument):
        self.options.add_argument(argument)

    def add_experimental_option(self, name, value):
        self.options.add_experimental_option(name=name, value=value)
