from selenium.webdriver import FirefoxProfile


class Profile(object):
    def __init__(self, profile: FirefoxProfile or str):
        self.profile = profile if isinstance(profile, FirefoxProfile) else FirefoxProfile(profile_directory=profile)

    def set_preference(self, key, value):
        self.profile.set_preference(key=key, value=value)
