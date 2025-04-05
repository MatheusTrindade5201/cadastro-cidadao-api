from typing import Optional

from pydantic import BaseModel

from persistency.schemas.user_schemas import RoleOptions


class LoginInput(BaseModel):
    username: str
    password: str


class LoginOutput(BaseModel):
    access_token: str


class MeOutput(BaseModel):
    id: int
    name: str
    email: str
    cpf: Optional[str]
    role: Optional[RoleOptions]

    class Config:
        orm_mode = True


class RecoveryPassword(BaseModel):
    email: str
    cpf: str


class NewPassword(BaseModel):
    password: str
    confirm_password: str
