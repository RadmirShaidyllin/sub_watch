from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from app.config import settings
from app.db.deps import get_db
from app.api.v1.auth.schemas import UserCreate, UserLogin, UserRead, TelegramAuth
from app.api.v1.auth.service import AuthService
from app.api.v1.auth.security import create_token, verify_telegram_auth

auth_router = APIRouter(prefix="/auth", tags=["Auth"])
service = AuthService()


@auth_router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(data: UserCreate, db: AsyncSession = Depends(get_db)):
    return await service.register(db, data.email, data.password)


@auth_router.post("/login")
async def login(
        db: Annotated[AsyncSession, Depends(get_db)],
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = await service.login(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_token({"sub": str(user.id)}, 15)
    refresh_token = create_token({"sub": str(user.id)}, 60 * 24 * 7)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": settings.token_type,
        "user": {
            "id": user.id,
            "email": user.email
        }
    }


@auth_router.post("/telegram-login")
async def telegram_login(data: TelegramAuth, db: AsyncSession = Depends(get_db)):
    if not verify_telegram_auth(data.model_dump(), settings.bot_token):
        raise HTTPException(status_code=400, detail="Invalid Telegram data")

    user = await service.login_or_register_telegram(db, data)

    access_token = create_token({"sub": str(user.id)}, 15)
    refresh_token = create_token({"sub": str(user.id)}, 60 * 24 * 7)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": settings.token_type,
        "user": UserRead.model_validate(user)
    }
