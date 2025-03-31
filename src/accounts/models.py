import datetime
from decimal import Decimal

from sqlalchemy import String, BigInteger, Numeric, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Account(Base):
    __tablename__ = 'accounts'

    id: Mapped[int] = mapped_column(primary_key=True)

    address: Mapped[str] = mapped_column(String(42), nullable=False)
    bandwidth: Mapped[int] = mapped_column(BigInteger, nullable=False)
    energy: Mapped[int] = mapped_column(BigInteger, nullable=False)
    balance: Mapped[Decimal] = mapped_column(Numeric, nullable=False)

    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True),
                                                          server_default=func.now(),
                                                          nullable=False)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id}, {self.address}, {self.created_at})'

    def __str__(self):
        return self.__repr__()
