from persistency.schemas.user_schemas import StatusOptions
from service.user_services import UserService
from utils.exceptions.exception import UserNotExists


async def get_user_by_id(user_id: int):
    user_exists = await UserService.get_user_by_id(user_id)

    if not user_exists or user_exists.status == StatusOptions.Erased:
        raise UserNotExists("User not exists")
