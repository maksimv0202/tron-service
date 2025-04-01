from decimal import Decimal

import pytest

from accounts.models import Account
from accounts.repositories import AccountRepository


@pytest.mark.asyncio
async def test_add_account(async_session):
    test_account = {
        'address': 'TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g',
        'bandwidth': 100,
        'energy': 0,
        'balance': Decimal('116152503.453803')
    }
    account = await AccountRepository(async_session).add(Account(**test_account))
    assert account.id is not None and account.id == 1

    accounts = await AccountRepository(async_session).get()

    assert len(accounts) == 1
    assert accounts[0].address == test_account['address']
    assert accounts[0].bandwidth == test_account['bandwidth']
    assert accounts[0].energy == test_account['energy']


@pytest.mark.asyncio
async def test_get_accounts(async_session):
    for i in range(25):
        test_account = {
            'address': f'TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsn7D{i}g',
            'bandwidth': i * 100,
            'energy': i * 200,
            'balance': Decimal(str(i * 9.01))
        }
        await AccountRepository(async_session).add(Account(**test_account))

    accounts = await AccountRepository(async_session).get()
    assert len(accounts) == 25

    total_count = await AccountRepository(async_session).get()
    assert len(total_count) == 25


@pytest.mark.asyncio
async def test_get_accounts_with_pagination(async_session):
    for i in range(1, 9):
        test_account = {
            'address': f'TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsn7D{i}g',
            'bandwidth': i * 100,
            'energy': i * 200,
            'balance': Decimal(str(i * 9.01))
        }
        await AccountRepository(async_session).add(Account(**test_account))

    page_1 = await AccountRepository(async_session).get(offset=1, limit=3)
    assert [account.id for account in page_1] == [1, 2, 3]

    page_2 = await AccountRepository(async_session).get(offset=2, limit=3)
    assert [account.id for account in page_2] == [4, 5, 6]

    page_3 = await AccountRepository(async_session).get(offset=3, limit=3)
    assert [account.id for account in page_3] == [7, 8]

