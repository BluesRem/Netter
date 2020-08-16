from selenium import webdriver


class Profile(object):
    def __init__(self, profile_directory=None):
        self.profile = webdriver.FirefoxProfile(profile_directory=profile_directory)

    def set_preference(self, key, value):
        self.profile.set_preference(key=key, value=value)

    def __call__(self, *args, **kwargs):
        return self.profile
