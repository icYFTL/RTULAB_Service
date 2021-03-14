import requests
from core import purchases_config


class PurchasesAPI:
    def __init__(self):
        self.host = purchases_config['host']

    def add_purchase(self, name: str, total: int, user_id: int, shop_id: int, method: str, category=None) -> int:
        r = requests.post(self.host + '/purchases/new_purchase', json={
            'name': name,
            'total': total,
            'user_id': user_id,
            'shop_id': shop_id,
            'method': method,
            'category': category
        })

        return r.status_code

