from typing import AsyncGenerator

import pytest_asyncio

from sqlalchemy import StaticPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from accounts.models import Base


@pytest_asyncio.fixture(scope='function')
async def async_engine():
    engine = create_async_engine(
        'sqlite+aiosqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@pytest_asyncio.fixture
async def async_session(async_engine) -> AsyncGenerator[AsyncSession, None]:
    async_session = async_sessionmaker(async_engine, autocommit=False, autoflush=False, expire_on_commit=False)
    async with async_session() as session:
        yield session
