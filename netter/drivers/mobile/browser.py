from appium.webdriver import Remote


class WebDriver(object):
    TYPE = 'Appium'

    def __init__(self, name, desired_capabilities: dict):
        desired_capabilities.setdefault('browserName', name)
        self.desired_capabilities = desired_capabilities

    def Remote(self, ip='127.0.0.1', port='4444'):
        return Remote(f'http://{ip}:{port}/wd/hub', desired_capabilities=self.desired_capabilities)
