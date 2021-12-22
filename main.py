from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import JSONResponse

from api import FRoidAPIError
from routers import users, posts
from routers.base import api_session

base_router = APIRouter(prefix="/v1")
# User related router
base_router.include_router(users.router)
# Every endpoint related to posts should be included in this router:
base_router.include_router(posts.router)

app = FastAPI(
    debug=True,  # Set debug to True to see the error message in the browser
    title="Froid API",
    version="1.0.0",
    description="An Unofficial Web API For [Farsroid](https://farsroid.com/) Website.",
    contact={"email": "IHosseini@pm.me"},
)
app.include_router(base_router)


# TODO: Handle exceptions for API and report them to the admin. 
@app.exception_handler(FRoidAPIError)
async def handle_api_error(_: Request, exc: FRoidAPIError):
    """Handle API errors."""
    # TODO: make specific error messages for each error code
    return JSONResponse(status_code=exc.code, content=exc.to_dict())


# TODO: Complete startup and shutdown events
@app.on_event("startup")
async def startup_event():
    ...


@app.on_event("shutdown")
async def shutdown_event():
    """Operations to perform when the server shuts down."""
    # TODO: close database connection and API session for requests
    await api_session.close()
