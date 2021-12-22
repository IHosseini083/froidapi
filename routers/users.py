from fastapi import APIRouter

from .models import RegisteredUser, UserRegister

router = APIRouter()


@router.post(
    "/register",
    response_model=RegisteredUser,
    summary="User registration",
    response_description="The user that was registered.",
    status_code=201
)
async def register_user(user: UserRegister) -> RegisteredUser:
    # TODO: implement user registration
    return RegisteredUser(username=user.username, email=user.email)
