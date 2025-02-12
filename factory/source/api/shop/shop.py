import requests
from core import shop_config
from .exceptions import NotAvailable
from random import choice


class ShopAPI:
    def __init__(self):
        self.host = shop_config['host']

    def is_available(self) -> bool:
        try:
            r = requests.get(self.host)
            if r.status_code != 200:
                raise NotAvailable()
            return True
        except:
            return False

    def __shops_online(fn):
        def f(self, *args, **kwargs):
            if not self.is_available():
                raise NotAvailable('Shop service is not available now')
            return fn(self, *args, **kwargs)

        return f

    def __get_shops(self) -> list:
        return requests.get(self.host + '/get_shops').json()['response']['result']

    @__shops_online
    def add_items(self, items: list) -> bool:
        shops = self.__get_shops()
        if not shops:
            return False

        shop = choice(shops)['id']

        r = requests.put(self.host + f'/{shop}/add_items', json={
            'items': [x.get_dict() for x in items]
        }, headers={'XXX-CODE': shop_config['password']})

        return r.status_code == 201
