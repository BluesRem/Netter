class Alert(object):
    def __init__(self, alert):
        self._alert = alert

    @property
    def message(self):
        return self._alert.text

    def accept(self):
        self._alert.accept()

    def dismiss(self):
        self._alert.dismiss()
