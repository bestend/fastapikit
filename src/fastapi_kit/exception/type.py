class BadRequestHeaderError(Exception):
    def __init__(self, exception: Exception | str = "") -> None:
        self.exception = exception

    def __str__(self) -> str:
        return str(self.exception)


class InvalidAccessTokenError(Exception):
    def __init__(self, exception: Exception | str = "") -> None:
        self.exception = exception

    def __str__(self) -> str:
        return str(self.exception)
