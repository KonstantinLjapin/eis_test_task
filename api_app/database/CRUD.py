from api_app.database.models import Base, User
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import select, update
from api_app.database.databese import DatabaseHelper
from api_app.database import schemas


async def base_create() -> None:
    db: DatabaseHelper = DatabaseHelper()
    engine: AsyncEngine = db.engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()
