from api_app.database.models import Base
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import select, update
from api_app.database.databese import DatabaseHelper
from api_app.database import schemas, models


async def create_user_item(db: DatabaseHelper, item: schemas.ItemBase) -> None:
    async_session = db.session_factory
    async with async_session() as session:
        async with session.begin():
            session.add(models.Item(title=item.title, description=item.description))
            stmt = select(models.Item)
            await session.execute(stmt)
            await session.commit()
