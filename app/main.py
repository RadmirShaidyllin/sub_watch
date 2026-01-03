from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import text

from app.config import settings
from app.db.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    print('FastAPI started')
    async with engine.begin() as conn:
        await conn.execute(text("SELECT 1"))
        print("DB connection OK")
    yield
    await engine.dispose()
    print('FastAPI stopped')


app = FastAPI(
    title=settings.app_name,
)


@app.get('/')
async def root():
    return {'messages': f'{settings.app_name}'}
