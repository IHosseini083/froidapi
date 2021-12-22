from typing import Any, Dict, Optional


class FRoidAPIError(Exception):
    """Base exception class for all the API errors."""

    def __init__(self, msg: str, code: Optional[int] = None) -> None:
        self.msg = msg
        self.code = code

    def to_dict(self) -> Dict[str, Any]:
        """Convert the exception to a dictionary."""
        return {
            "status": self.code,
            "message": self.msg,
        }


class NotFoundError(FRoidAPIError):
    """Raised when a resource is not found."""


class AccessDeniedError(FRoidAPIError):
    """Raised when access to a resource is denied by the server."""


class ResponseError(FRoidAPIError):
    """Raised when the response is not valid and cannot be parsed."""


class BadRequestError(FRoidAPIError):
    """Raised when the request is invalid."""
