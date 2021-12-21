from fastapi import FastAPI

from routers.base import base_router

app = FastAPI(
    title="Froid API",
    version="1.0.0",
    description="An Unofficial Web API For [Farsroid](https://farsroid.com/) Website.",
    contact={"email": "IHosseini@pm.me"},
)
app.include_router(base_router)


# TODO: Complete startup and shutdown events
@app.on_event("startup")
async def startup_event():
    print("Startup event")
    

@app.on_event("shutdown")
async def shutdown_event():
    # TODO: close database connection and API session for requests
    print("Shutdown event")
