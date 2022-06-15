class HTTPRequestError(Exception):

    def __init__(self, url: str, code: int, msg: str = None):
        self.url = url
        self.code = code
        self.msg = code

    def __str__(self) -> str:
        """
        Convert the exception into a printable string
        """
        return f"Request to {self.url!r} failed. Code: {self.code}; Message: {self.msg}"
