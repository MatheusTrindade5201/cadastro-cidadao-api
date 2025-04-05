from datetime import datetime

from sqlalchemy import insert, select, update
from sqlalchemy.sql import and_, or_

from persistency.models.models import  User
from persistency.schemas.user_schemas import (
    StatusOptions,
    UserInput,
    UserUpdateInput,
)
from utils.middlewares.session_controller import (
    QueryResponseOptions,
    ReadDatabaseSession,
    WriteDatabaseSession,
)
from utils.providers.hash_provider import generate_hash


class UserService:
    @WriteDatabaseSession
    async def create_user(self: UserInput):
        query = insert(User).values(
            {
                "name": self.name,
                "cpf": self.cpf,
                "email": self.email,
                "password": generate_hash(self.password),
                "created_at": self.created_at,
                "role": self.role,
            }
        )
        return query

    @ReadDatabaseSession(QueryResponseOptions.First)
    async def get_user(self: str):
        query = select(User).where(
            and_(
                User.email == self,
                User.status != StatusOptions.Erased,
            )
        )
        return query

    @staticmethod
    @ReadDatabaseSession(QueryResponseOptions.All)
    async def get_users():
        query = select(User).where(User.status == StatusOptions.Active)

        return query

    @ReadDatabaseSession(QueryResponseOptions.First)
    async def get_user_by_id(id: int):
        query = select(User).where(User.id == id)
        return query

    @WriteDatabaseSession
    async def delete_user(id: int):
        query = (
            update(User)
            .where(User.id == id)
            .values(
                {"status": StatusOptions.Erased, "deleted_at": datetime.now()}
            )
        )
        return query

    @WriteDatabaseSession
    async def update_user(id: int, user: UserUpdateInput):
        query = (
            update(User)
            .where(and_(User.id == id, User.status != StatusOptions.Erased))
            .values(
                name=user.name or User.name,
                cep=user.cep or User.cep,
                city=user.city or User.city,
                street=user.street or User.street,
                district=user.district or User.district,
                number=user.number or User.number,
                birthday=user.birthday or User.birthday,
                updated_at=datetime.now(),
            )
        )
        return query

    @WriteDatabaseSession
    async def update_password(email: str, password: str, salt: str = None):
        query = (
            update(User)
            .where(
                and_(User.email == email, User.status != StatusOptions.Erased)
            )
            .values(
                {
                    "password": generate_hash(password),
                    "salt": salt or User.salt,
                    "updated_at": datetime.now(),
                }
            )
        )
        return query

    @WriteDatabaseSession
    async def update_status(email: str, salt: str):
        query = (
            update(User)
            .where(
                and_(User.email == email, User.status != StatusOptions.Erased)
            )
            .values(
                {
                    "status": StatusOptions.Active,
                    "salt": salt,
                    "updated_at": datetime.now(),
                }
            )
        )
        return query
