from httpx import AsyncClient


class AsyncTronGrid:

    __slots__ = ('client', 'headers')

    def __init__(self, client: AsyncClient):
        self.client = client
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    async def get_account(self, address: str) -> dict:
        response = await self.client.post(
            url='https://api.trongrid.io/wallet/getaccount',
            json={'address': address, 'visible': True},
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    async def get_account_resource(self, address: str) -> dict:
        response = await self.client.post(
            url='https://api.trongrid.io/wallet/getaccountresource',
            json={'address': address, 'visible': True},
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
