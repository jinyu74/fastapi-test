from datetime import datetime
from enum import Enum
from typing import List
from pydantic import BaseModel, EmailStr


class Gender(str, Enum):
    male = "male"
    female = "female"


class Role(str, Enum):
    admin = "admin"
    user = "user"
    student = "student"


class User(BaseModel):
    id: EmailStr
    first_name: str
    last_name: str
    middle_name: str | None
    gender: Gender
    roles: List[Role]
    password: str


class UserPayload(User):
    exp: datetime


class UserUpdateRequest(BaseModel):
    first_name: str | None
    last_name: str | None
    middle_name: str | None
    roles: List[Role] | None
