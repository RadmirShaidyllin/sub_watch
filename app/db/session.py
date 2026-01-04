from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from app.config import settings

url = str(settings.async_database_url)

engine = create_async_engine(
    url,
    echo=True,
)

async_session_maker = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)
