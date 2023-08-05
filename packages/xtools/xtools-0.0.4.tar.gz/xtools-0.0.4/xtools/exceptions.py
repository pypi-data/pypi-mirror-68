from typing import Optional


class BaseXToolsException(Exception):
    def __init__(self, message, code: Optional[int] = None):
        super().__init__(message)
        self.code = code


class NotFound(BaseXToolsException):
    pass


class TooManyEdits(BaseXToolsException):
    pass