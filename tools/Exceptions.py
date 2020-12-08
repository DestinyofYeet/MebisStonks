class SettingNotFoundError(Exception):
    def __init__(self, message):
        super().__init__(message)


class InvalidSettingError(Exception):
    def __init__(self, message):
        super().__init__(message)
