import datetime
from decimal import Decimal

from pydantic import BaseModel


class AccountSchema(BaseModel):
    id: int
    address: str
    bandwidth: int
    energy: int
    balance: Decimal
    created_at: datetime.datetime


class AccountResponseSchema(BaseModel):
    address: str
    bandwidth: int
    energy: int
    balance: Decimal
