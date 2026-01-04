from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.deps import get_db
from app.auth.schemas import UserCreate, UserLogin, UserRead
from app.auth.service import AuthService
from app.auth.security import create_token


auth_router = APIRouter(prefix="/auth", tags=["Auth"])
service = AuthService()


@auth_router.post("/register", response_model=UserRead)
async def register(data: UserCreate, db: AsyncSession = Depends(get_db)):
    return await service.register(db, data.email, data.password)


@auth_router.post("/login")
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    user = await service.login(db, data.email, data.password)

    return {
        "access": create_token({"sub": str(user.id)}, 15),
        "refresh": create_token({"sub": str(user.id)}, 60 * 24 * 7)
    }
