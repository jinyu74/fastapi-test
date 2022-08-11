from enum import Enum
from typing import List
from uuid import UUID, uuid4
from pydantic import BaseModel


class Gender(str, Enum):
    male = "male"
    female = "female"


class Role(str, Enum):
    admin = "admin"
    user = "user"
    student = "student"


class User(BaseModel):
    id: UUID | None = uuid4()
    first_name: str
    last_name: str
    middle_name: str | None
    gender: Gender
    roles: List[Role]


class UserUpdateRequest(BaseModel):
    first_name: str | None
    last_name: str | None
    middle_name: str | None
    roles: List[Role] | None
