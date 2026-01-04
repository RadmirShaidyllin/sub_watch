from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.v1.auth.models import User


class UserRepository:
    async def get_by_email(self, db: AsyncSession, email: str):
        q = select(User).where(User.email == email)
        return (await db.execute(q)).scalar_one_or_none()

    async def get_by_tg(self, db: AsyncSession, tg_id: int):
        q = select(User).where(User.tg_id == tg_id)
        return (await db.execute(q)).scalar_one_or_none()

    async def create(self, db: AsyncSession, user: User):
        await user.save(db)
        return user
