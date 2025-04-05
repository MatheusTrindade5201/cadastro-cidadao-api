from typing import List

from fastapi import APIRouter, Depends

from logic.user_logic import UserLogic
from service.user_services import UserService
from persistency.connection import get_db
from persistency.schemas.login_schemas import MeOutput
from persistency.schemas.user_schemas import (
    ChangePasswordInput,
    UserInput,
    UserOutput,
    UserOutputOnCreate,
    UserUpdateInput,
)
from utils.helpers.user_helpers.change_password_validator import change_password_validator
from utils.helpers.user_helpers.get_user_by_id import get_user_by_id
from utils.helpers.validators.token_validator import (
    validate_session,
    validate_session_admin,
)


user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.get(
    "/me",
    description="Route to get about me",
    status_code=200,
    response_model=MeOutput,
    dependencies=[Depends(get_db)],
)
async def me(payload=Depends(validate_session)):
    user = await UserService.get_user(payload.get("sub"))
    return user


@user_router.get(
    "/",
    description="Route to read all users",
    status_code=200,
    response_model=List[UserOutput],
    dependencies=[Depends(get_db)],
)
async def get_user_db():
    # Get all users on database.
    user = await UserService.get_users()
    return user


@user_router.post(
    "/",
    description="Route to add new users",
    status_code=201,
    response_model=UserOutputOnCreate,
    dependencies=[Depends(get_db)],
)
async def create_user(user: UserInput):
    return await UserLogic.create_user_logic(user)


@user_router.delete(
    "/{user_id}",
    description="Route to delete one users",
    status_code=204,
    dependencies=[Depends(get_db), Depends(validate_session_admin)],
)
async def delete_user_by_id(user_id: int):
    await get_user_by_id(user_id)

    await UserService.delete_user(user_id)
    return


@user_router.patch(
    "/change_password",
    description="Route to change password",
    status_code=204,
    dependencies=[Depends(get_db)],
)
async def change_password(
    passwords: ChangePasswordInput, payload=Depends(validate_session)
):
    user = await UserService.get_user(payload.get("sub"))

    await change_password_validator(passwords, user)

    await UserService.update_password(user.email, passwords.new_password)


@user_router.patch(
    "/{user_id}",
    description="Route to update one user",
    status_code=204,
    dependencies=[Depends(get_db), Depends(validate_session)],
)
async def update_user(
    user_id: int,
    user: UserUpdateInput,
):
    await get_user_by_id(user_id)
    await UserService.update_user(user_id, user)
    return
