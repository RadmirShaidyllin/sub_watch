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
