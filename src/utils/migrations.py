import asyncio
import functools

from contextlib import asynccontextmanager

from alembic.config import Config
from alembic import command
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    await asyncio.to_thread(functools.partial(command.upgrade, Config('alembic.ini'), 'head'))
    yield
