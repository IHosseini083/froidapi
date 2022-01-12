from typing import Any, Callable

from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

import cfg
from api import FRoidAPIError, ParserError
from database import db
from routers import posts, users
from routers.base import api_handler, raise_error

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

# Define metadata for the swagger API tags
endpoint_tags = [
    {
        "name": "Users",
        "description": "User related endpoints (login, register, etc.)",
    },
    {
        "name": "Posts",
        "description": "Get information about posts and their properties.",
    }
]

app = FastAPI(
    debug=cfg.DEBUG,  # Set debug to True to see the error message in the browser
    title=cfg.APP_NAME,
    version=cfg.APP_VERSION,
    description=cfg.APP_DESCRIPTION,
    contact=cfg.CONTACT_INFO,
    openapi_tags=endpoint_tags,
    openapi_url=cfg.OPENAPI_URL,
    redoc_url=None,  # Disable the redoc_url to avoid the redoc-ui to be loaded
)
app.include_router(base_router)
# mount the static files path
app.mount("/static", StaticFiles(directory="static"), name="static")
# add CORS middleware to the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=cfg.ORIGINS,
    allow_credentials=cfg.ALLOW_CREDENTIALS,
    allow_methods=cfg.ALLOW_METHODS,
    allow_headers=cfg.ALLOW_HEADERS,
)


# override the default settings for the swagger UI
@app.get(cfg.DOCS_URL, include_in_schema=False)
def overridden_swagger_docs() -> HTMLResponse:
    """Override the default swagger UI settings."""
    return get_swagger_ui_html(
        openapi_url=cfg.OPENAPI_URL,
        title=cfg.DOCS_TITLE,
        swagger_favicon_url=cfg.DOCS_FAVICON_URL
    )


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


# handle API parser errors
@app.exception_handler(ParserError)
async def handle_parser_error(_: Request, __: ParserError) -> None:
    """Handle parser errors."""
    raise_error(500, message="Internal server error")


# TODO: Complete startup and shutdown events
@app.on_event("startup")
async def startup_event() -> None:
    # Initialize the database connection
    db.init_db()


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """Operations to perform when the server shuts down."""
    # TODO: close database connection and API session for requests
    await api_handler.close()
