from sqlalchemy.ext.asyncio import AsyncSession, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class Base(AsyncAttrs, DeclarativeBase):

    async def save(self, db: AsyncSession):
        db.add(self)
        await db.flush()
        return self

    @classmethod
    async def find_by_id(cls, db: AsyncSession, id: int):
        return await db.get(cls, id)
