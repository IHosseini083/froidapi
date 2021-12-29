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
    if not isinstance(headers, dict):
        raise ValueError("headers must be a dictionary")
    raise HTTPException(status_code=error_code, detail=kwargs, headers=headers)
