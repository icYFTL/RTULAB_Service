from threading import Thread, Lock
from ..database import *
from ..api.shop import *
from random import randint, choice
from time import sleep


class Provider(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.state = 'offline'
        self.status = 'preparing'
        self.lock = Lock()
        self.delay = 1800
        self.unsynced = 0

    def run(self) -> None:
        self.state = 'online'
        item_methods = methods.ItemMethods()

        while True:
            if self.lock.locked():
                self.status = 'locked'
                self.lock.acquire()
            items = [x for x in item_methods.get_items() if x.count > 0]
            sorted_items = []
            while len(items) > 1:
                _right = randint(1, len(items) - 1)
                sorted_items.append(items[:_right])
                del items[:_right]

            if sorted_items:
                choice(sorted_items).append(items[0])

            del items

            shop = ShopAPI()

            for _items in sorted_items:
                try:
                    if shop.add_items(_items):
                        [item_methods.clear_item(item) for item in _items]
                    self.unsynced = 0
                except exceptions.NotAvailable:
                    self.unsynced = sum([len(x) for x in sorted_items])
                    break

            self.status = f'sleep for {self.delay} seconds'
            sleep(self.delay)
