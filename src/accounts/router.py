from typing import Any

import httpx

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from accounts.models import Account
from accounts.repositories import AccountRepository
from accounts.schemas import AccountSchema, AccountResponseSchema
from accounts.service import AsyncTronGrid, AccountService
from db import get_async_session
from utils.schemas import PaginatedResponseSchema

router = APIRouter()


@router.post('/accounts/{address}', response_model=AccountResponseSchema)
async def get_account(address: str, session: AsyncSession = Depends(get_async_session)) -> Any:
    async with httpx.AsyncClient() as client:
        async_tron_grid = AsyncTronGrid(client)

        account_balance = await async_tron_grid.get_account_balance(address)
        await async_tron_grid.get_account_resource(address)

        bandwidth = async_tron_grid.get_account_bandwidth()
        energy = async_tron_grid.get_account_energy()

        return await AccountRepository(session).add(Account(
            address=address,
            bandwidth=bandwidth,
            energy=energy,
            balance=account_balance
        ))


@router.get('/requests', response_model=PaginatedResponseSchema[AccountSchema])
async def get_requests(
        page: int = Query(ge=1, default=1),
        size: int = Query(ge=1, le=100, default=100),
        session: AsyncSession = Depends(get_async_session)) -> Any:
    return await AccountService(AccountRepository(session)).get_paginated(page, size)
