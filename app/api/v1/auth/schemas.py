import typing as t
from pydantic import BaseModel, EmailStr

if t.TYPE_CHECKING:
    EmailStr = t.Annotated[str, ...]


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    email: EmailStr | None
    is_active: bool

    class Config:
        from_attributes = True

class TelegramAuth(BaseModel):
    id: int
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    photo_url: str | None = None
    auth_date: int
    hash: str
