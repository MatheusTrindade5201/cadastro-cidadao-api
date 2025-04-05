from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class RoleOptions(str, Enum):
    Default = "default"
    Admin = "admin"


class StatusOptions(int, Enum):
    Erased = -1
    Inactive = 0
    Active = 1


class UserInput(BaseModel):
    name: str
    cpf: str
    email: str
    password: str
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    cep: Optional[str] = None
    city: Optional[str] = None
    street: Optional[str] = None
    district: Optional[str] = None
    number: Optional[str] = None
    role: Optional[RoleOptions] = RoleOptions.Default
    birthday: Optional[date] = None


class UserOutput(BaseModel):
    id: int
    name: str
    email: str
    role: str
    status: int

    class Config:
        orm_mode = True


class UserOutputOnCreate(BaseModel):
    name: str
    cpf: str
    email: str
    role: str
    created_at: datetime

    class Config:
        orm_mode = True


class UserUpdateInput(BaseModel):
    name: Optional[str]
    cep: Optional[str]
    city: Optional[str]
    street: Optional[str]
    district: Optional[str]
    number: Optional[str]
    birthday: Optional[date]

    class Config:
        orm_mode = True


class UserOutputPayments(BaseModel):
    order_id: str
    status: str
    datetime: datetime
    value: int

    class Config:
        orm_mode = True


class ChangePasswordInput(BaseModel):
    old_password: str
    new_password: str
    confirm_new_password: str
