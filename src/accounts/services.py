import math
from decimal import Decimal

from httpx import AsyncClient

from exceptions import HTTP404StatusError
from accounts.repositories import AccountRepository
from accounts.models import Account


class AsyncTronGrid:
    """

   address: A TRON address is a 42-character string that begins with the letter "T"

   bandwidth (Account Bandwidth Balance Query): First, call the node
   HTTP interface /wallet/getaccountresource to obtain the current
   resource status of the account, and then calculate the bandwidth
   balance by the following formula:
   - Free bandwidth balance (int64) = freeNetLimit - freeNetUsed
   - Bandwidth balance obtained by staking TRX = NetLimit - NetUsed

   energy: First call the node HTTP interface /wallet/getaccountresource
   to obtain the current resource status of the account, and then
   calculate the energy balance by the following formula:
   - Energy Balance (int64) = EnergyLimit (int64) - EnergyUsed (int64)

   balance:

   Source: https://tronprotocol.github.io/documentation-en/mechanism-algorithm/resource/
   """

    __slots__ = ('client', 'headers', 'resource')

    def __init__(self, client: AsyncClient):
        self.client = client
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        self.resource = {}

    async def get_account(self, address: str) -> dict:
        response = await self.client.post(
            url='https://api.trongrid.io/wallet/getaccount',
            json={'address': address, 'visible': True},
            headers=self.headers
        )
        response.raise_for_status()
        if response.json().get('Error', None):
            raise HTTP404StatusError
        return response.json()

    async def get_account_resource(self, address: str) -> dict:
        response = await self.client.post(
            url='https://api.trongrid.io/wallet/getaccountresource',
            json={'address': address, 'visible': True},
            headers=self.headers
        )
        response.raise_for_status()
        self.resource = response.json()
        return self.resource

    async def get_account_balance(self, address: str) -> Decimal:
        account = await self.get_account(address)
        return Decimal(account.get('balance', 0)) / 1_000_000

    def get_account_bandwidth(self) -> int:
        return (self.resource.get('freeNetLimit', 0) - self.resource.get('freeNetUsed', 0)
                + self.resource.get('NetLimit', 0) - self.resource.get('NetUsed', 0))

    def get_account_energy(self) -> int:
        return self.resource.get('EnergyLimit', 0) - self.resource.get('EnergyUsed', 0)


class AccountService:

    def __init__(self, repository: AccountRepository):
        self._repository = repository

    async def add_account(self, account: Account) -> Account:
        return await self._repository.add(account)

    async def get_paginated(self, page: int, size: int):
        data = await self._repository.get(page, size)
        total = await self._repository.get_total_count()
        pages = math.ceil(total / size) if total > 0 else 0
        return {
            'data': data,
            'total': total,
            '_meta': {
                'page': page,
                'next': page + 1 if page < pages else None,
                'prev': page - 1 if page > 1 else None
            },
        }
