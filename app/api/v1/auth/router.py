from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db.deps import get_db
from app.api.v1.auth.schemas import UserCreate, UserLogin, UserRead
from app.api.v1.auth.service import AuthService
from app.api.v1.auth.security import create_token

auth_router = APIRouter(prefix="/auth", tags=["Auth"])
service = AuthService()


@auth_router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(data: UserCreate, db: AsyncSession = Depends(get_db)):
    return await service.register(db, data.email, data.password)


@auth_router.post("/login")
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    user = await service.login(db, data.email, data.password)

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
