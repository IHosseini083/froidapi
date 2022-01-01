from typing import Any, Callable

from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from api import FRoidAPIError
from routers import posts, users
from routers.base import api_session

base_router = APIRouter(
    prefix="/v1",
    responses={
        400: {"description": "Bad request, invalid parameters were sent."},
        404: {"description": "Not found, the requested resource/post was not found."},
    }
)
# User related router
base_router.include_router(users.router)
# Every endpoint related to posts should be included in this router:
base_router.include_router(posts.router)

app = FastAPI(
    debug=True,  # Set debug to True to see the error message in the browser
    title="Froid API",
    version="1.0.0",
    description="An Unofficial Web API For [Farsroid](https://farsroid.com/) Website.",
    contact={"email": "IHosseini@pm.me"}
)
app.include_router(base_router)


# TODO: expand this middleware to handle every request and response
@app.middleware("http")
async def get_current_request(request: Request, call_next: Callable[..., Any]) -> Any:
    return await call_next(request)
    

# TODO: Handle exceptions for API and report them to the admin. 
@app.exception_handler(FRoidAPIError)
async def handle_api_error(_: Request, exc: FRoidAPIError) -> JSONResponse:
    """Handle API errors."""
    # TODO: make specific error messages for each error code
    return JSONResponse(status_code=exc.code, content=exc.to_dict())


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(_: Request, exc: StarletteHTTPException) -> JSONResponse:
    """Handle HTTP exceptions."""
    # dummy handler for now. Maybe we'll add more handlers later.
    if not isinstance(exc.detail, dict):
        exc.detail = {"detail": exc.detail}
    if not exc.detail.get("status"):
        # The same 'status' key is used in the API error 'to_dict' method.
        exc.detail["status"] = exc.status_code
    return JSONResponse(status_code=exc.status_code, content=exc.detail)


# TODO: Complete startup and shutdown events
@app.on_event("startup")
async def startup_event() -> None:
    ...


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """Operations to perform when the server shuts down."""
    # TODO: close database connection and API session for requests
    await api_session.close()
