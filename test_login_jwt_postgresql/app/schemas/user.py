from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    is_active: bool | None = True
    is_superuser: bool | None = False


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: str | None = None


class UserInDBBase(UserBase):
    id: int
    password: str | None = None

    class Config:
        orm_mode = True


class UserRead(UserInDBBase):
    pass
