import requests
from core import purchases_config


class PurchasesAPI:
    def __init__(self):
        self.host = purchases_config['host']

    def is_available(self) -> bool:
        try:
            return requests.get(self.host).status_code == 200
        except:
            return False

    def add_purchase(self, name: str, total: int, user_id: int, shop_id: int, method: str, category=None) -> int:
        try:
            r = requests.post(self.host + '/purchases/new_purchase', json={
                'name': name,
                'total': total,
                'user_id': user_id,
                'shop_id': shop_id,
                'method': method,
                'category': category
            })
        except:
            return 500

        return r.status_code

