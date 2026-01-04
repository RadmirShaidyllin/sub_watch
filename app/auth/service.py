from fastapi import HTTPException
from app.auth.repository import UserRepository
from app.auth.models import User
from app.auth.security import hash_password, verify_password


class AuthService:
    def __init__(self):
        self.repo = UserRepository()

    async def register(self, db, email, password):
        existing = await self.repo.get_by_email(db, email)
        if existing:
            raise HTTPException(status_code=400, detail="User already exists")

        user = User(
            email=email,
            hashed_password=hash_password(password)
        )

        return await self.repo.create(db, user)

    async def login(self, db, email, password):
        user = await self.repo.get_by_email(db, email)

        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        return user

    async def login_telegram(self, db, tg_id: int):
        user = await self.repo.get_by_tg(db, tg_id)

        if not user:
            user = User(tg_id=tg_id)
            await self.repo.create(db, user)

        return user
