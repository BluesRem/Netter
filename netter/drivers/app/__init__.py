from appium.webdriver import Remote


class WebDriver(object):
    def __init__(self, desired_capabilities: dict):
        self.desired_capabilities = desired_capabilities

    def remote(self, host='127.0.0.1', port='4444'):
        return Remote(f'http://{host}:{port}/wd/hub', desired_capabilities=self.desired_capabilities)
