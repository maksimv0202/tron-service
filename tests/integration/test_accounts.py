from decimal import Decimal
from unittest.mock import AsyncMock, Mock
import pytest

from fastapi import status

from accounts.models import Account
from accounts.repositories import AccountRepository


@pytest.mark.asyncio
async def test_get_requests_paginated_with_no_accounts(async_client):
    response = await async_client.get('/requests', params={'page': 1, 'size': 1})
    accounts = response.json()
    assert accounts != {}
    assert response.status_code == status.HTTP_200_OK

    assert '_meta' in accounts
    assert 'data' in accounts

    assert accounts['data'] == []
    assert accounts['total'] == 0
    assert accounts['_meta'] == {'page': 1, 'next': None, 'prev': None}


@pytest.mark.asyncio
async def test_get_requests_paginated(async_client, async_session):
    for i in range(25):
        test_account = {
            'address': f'TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsn7D{i}g',
            'bandwidth': i * 100,
            'energy': i * 200,
            'balance': Decimal(str(i * 9.01))
        }
        await AccountRepository(async_session).add(Account(**test_account))

    response = await async_client.get('/requests', params={'page': 1, 'size': 5})
    accounts = response.json()
    assert accounts != {}
    assert response.status_code == status.HTTP_200_OK

    assert accounts['data'] != []
    assert accounts['total'] == 25
    assert accounts['_meta'] == {'page': 1, 'next': 2, 'prev': None}


@pytest.mark.asyncio
async def test_get_account(mocker, async_client, async_session):
    test_account = {
        'address': 'TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g',
        'bandwidth': 100,
        'energy': 0,
        'balance': Decimal('116152503.453803')
    }
    mock_async_tron_grid = mocker.patch('accounts.router.AsyncTronGrid', autospec=True)

    mock = mock_async_tron_grid.return_value

    mock.get_account_balance = AsyncMock(return_value=test_account['balance'])
    mock.get_account_resource = AsyncMock(return_value=None)
    mock.get_account_bandwidth = Mock(return_value=test_account['bandwidth'])
    mock.get_account_energy = Mock(return_value=test_account['energy'])

    response = await async_client.post('/accounts/{}'.format(test_account['address']))

    account = response.json()
    assert account != {}
    assert response.status_code == status.HTTP_200_OK

    assert account['address'] == test_account['address']
    assert account['bandwidth'] == test_account['bandwidth']
    assert account['energy'] == test_account['energy']

    total_count = await AccountRepository(async_session).get()
    assert len(total_count) == 1
