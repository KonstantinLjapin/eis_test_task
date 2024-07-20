from api_app.config import db_settings
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine
from typing import AsyncGenerator


def make_connection_string() -> str:
    """
    Make connection string to db
    """
    asyncpg_engine: str = "asyncpg"
    return (f"postgresql+{asyncpg_engine}://{db_settings.postgres_user}:{db_settings.postgres_password}@"
            f"{db_settings.postgres_host}:{db_settings.postgres_port}/{db_settings.postgres_db}")


class DatabaseHelper:
    def __init__(
            self,
            url: str = make_connection_string(),
            echo: bool = False,
            echo_pool: bool = False,
            pool_size: int = 5,
            max_overflow: int = 10,
    ) -> None:
        self.engine: AsyncEngine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def dispose(self) -> None:
        await self.engine.dispose()

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session


