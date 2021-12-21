from typing import Optional


class FRoidAPIError(Exception):
    """Base exception class for all the api errors."""

    def __init__(self, msg: str, code: Optional[int] = None) -> None:
        self.msg = msg
        self.code = code


class NotFoundError(FRoidAPIError):
    """Raised when a resource is not found."""


class AccessDeniedError(FRoidAPIError):
    """Raised when access to a resource is denied by the server."""


class ResponseError(FRoidAPIError):
    """Raised when the response is not valid and cannot be parsed."""
