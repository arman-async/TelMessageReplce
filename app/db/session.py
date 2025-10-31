from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app import config

from .models import Base
engine = create_async_engine(
    config.Database().uri(),
    pool_size=128,         # default: 5 → increase to handle more concurrent tasks
    max_overflow=60,      # allows up to 50 total (20 + 30)
    pool_timeout=30,      # how long to wait before raising TimeoutError
    pool_recycle=1800,    # recycle connections every 30 min
    pool_pre_ping=True,   # check connection health before using
)

SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


@asynccontextmanager
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    db = SessionLocal()
    try:
        yield db
    except Exception:
        await db.rollback()
        raise
    else:
        await db.commit()
    finally:
        await db.close()


async def get_db_session_depend() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


async def create_all_tables(engine: AsyncEngine = engine):
    """
    Create all tables defined in Base metadata asynchronously.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()