from typing import Dict, Any, Optional

from aiohttp import ClientSession
from fastapi.exceptions import HTTPException

from api import APIHandler as FroidAPIHandler

api_session = ClientSession()
api_handler = FroidAPIHandler(api_session)


def raise_error(error_code: int, headers: Optional[Dict[str, Any]] = None, **kwargs) -> None:
    """Raise an error with the given error code and arguments."""
    if not isinstance(error_code, int):
        raise ValueError("error_code must be an integer")
    if headers and not isinstance(headers, dict):
        raise ValueError("headers must be a dictionary")
    # add a 'error' parameter to the kwargs based on the error code
    error_fields = {
        400: "BAD_REQUEST",
        401: "UNAUTHORIZED",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
        405: "METHOD_NOT_ALLOWED",
        500: "INTERNAL_SERVER_ERROR",
    }
    kwargs["error"] = error_fields.get(error_code, "UNKNOWN_ERROR")
    raise HTTPException(status_code=error_code, detail=kwargs, headers=headers)
