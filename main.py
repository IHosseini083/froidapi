from fastapi import APIRouter, FastAPI

from routers import search, users
from routers.base import api_session

base_router = APIRouter(prefix="/v1")
base_router.include_router(users.router, tags=["users"], prefix="/users")
base_router.include_router(search.router, tags=["search"], prefix="/search")

app = FastAPI(
    debug=True,  # Set debug to True to see the error message in the browser
    title="Froid API",
    version="1.0.0",
    description="An Unofficial Web API For [Farsroid](https://farsroid.com/) Website.",
    contact={"email": "IHosseini@pm.me"},
)
app.include_router(base_router)


# TODO: Complete startup and shutdown events
@app.on_event("startup")
async def startup_event():
    ...
    

@app.on_event("shutdown")
async def shutdown_event():
    """Operations to perform when the server shuts down."""
    # TODO: close database connection and API session for requests
    await api_session.close()
