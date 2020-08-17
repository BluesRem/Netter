PLATFORM = {
    'iOS': 'iOS',
    'Android': 'Android',
    'win32': 'Windows',
    'linux': 'Linux',
    'darwin': 'Mac'
}


class Custom(object):

    def __init__(self, driver, type_, name_):
        self.type = type_
        self.name = name_
        self.os = PLATFORM[driver.capabilities.get('platformName')]
