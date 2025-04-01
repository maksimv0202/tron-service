import random

from locust import HttpUser, task, between


class AccountsUser(HttpUser):
    wait_time = between(1, 5)

    TRON_ADDRESSES = [
        'TRQaWxW1u8XxsK6NGxBtkFKU99yDUGdSwD',
        'TWF6ZTQVaVfsqaVd9cskvsnnoL7GTbNnzK',
        'TWzpz28NdMt32BpwYXG4DLbSxz1vzTPX1y',
        'TDToUxX8sH4z6moQpK3ZLAN24eupu2ivA4',
        'TDqSquXBgUCLYvYC4XZgrprLK589dkhSCf',
        'TTd9qHyjqiUkfTxe3gotbuTMpjU8LEbpkN',
        'TYukBQZ2XXCcRCReAUguyXncCWNY9CEiDQ',
        'TE4CRGTXpLR3eRsn2mNKwsJWBFT7ojtvnU',
        'TEBBKPZExaKwGKLTprC8jzh9qCZHF4teCr',
        'TXuCjfRTJ1D6bpGwCjqw5uChk7SGMnq8cc',
    ]

    @task
    def get_account(self):
        address = random.choice(self.TRON_ADDRESSES)
        self.client.post(f'/api/v1/accounts/{address}')


class RequestsUser(HttpUser):

    wait_time = between(1, 5)

    @task
    def get_requests(self):
        response = self.client.get('/api/v1/requests', params={'page': 1, 'limit': 1})
        total = response.json().get('total', 0)
        if response.status_code == 200:
            if not total:
                return
            else:
                limit = 80
                total_pages = (total + limit - 1) // limit
                for page in range(1, total_pages + 1):
                    self.client.get('/api/v1/requests', params={'page': page, 'limit': limit})
