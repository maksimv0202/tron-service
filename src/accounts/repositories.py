import abc

from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from accounts.models import Account


class SQLAlchemyAbstractRepository(abc.ABC):

    def __init__(self, session: AsyncSession):
        self._session = session


class AccountRepository(SQLAlchemyAbstractRepository):

    async def add(self, model: Account) -> Account:
        try:
            async with self._session.begin():
                self._session.add(model)
                await self._session.flush()
                await self._session.refresh(model)
            return model
        except (SQLAlchemyError, Exception) as e:
            raise RuntimeError(e)

    async def get(self, offset: int = None, limit: int = None) -> list[Account]:
        try:
            q = select(Account).order_by(Account.id)
            if offset and limit:
                offset_min = (offset - 1) * limit
                q = q.offset(offset_min).limit(limit)
            result = await self._session.execute(q)
            return list(result.scalars().all())
        except (SQLAlchemyError, Exception) as e:
            raise RuntimeError(e)

    async def get_total_count(self) -> int:
        result = await self._session.execute(select(func.count()).select_from(Account))
        return result.scalar_one()
