from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.auth.repository import UserRepository
from app.api.v1.auth.models import User
from app.api.v1.auth.security import hash_password, verify_password


class AuthService:
    def __init__(self):
        self.repo = UserRepository()

    async def register(self, db: AsyncSession, email: str, password: str):
        existing = await self.repo.get_by_email(db, email)
        if existing:
            raise HTTPException(status_code=400, detail="User already exists")

        user = User(
            email=email,
            hashed_password=hash_password(password),
            is_active=True
        )
        return await self.repo.create(db, user)

    async def login(self, db: AsyncSession, email: str, password: str):
        user = await self.repo.get_by_email(db, email)

        if not user or not user.hashed_password:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        return user

    async def login_telegram(self, db: AsyncSession, tg_id: int):
        user = await self.repo.get_by_tg(db, tg_id)

        if not user:
            user = User(tg_id=tg_id, is_active=True)
            user = await self.repo.create(db, user)

        return user
