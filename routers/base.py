from fastapi import APIRouter

from .users import users_router

# TODO: add dependencies for routers in base router
base_router = APIRouter(prefix="/v1")
base_router.include_router(users_router)
