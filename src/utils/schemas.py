from typing import Generic, TypeVar
from pydantic import BaseModel, Field


T = TypeVar('T', bound=BaseModel)


class PaginatedMetaSchema(BaseModel):
    page: int
    next: int | None
    prev: int | None


class PaginatedResponseSchema(BaseModel, Generic[T]):
    data: list[T]
    total: int
    meta: PaginatedMetaSchema = Field(alias='_meta')
