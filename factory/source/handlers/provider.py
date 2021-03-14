from threading import Thread
from ..database import *
from ..api.shop import *
from random import randint, choice
from time import sleep


class Provider(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self) -> None:
        item_methods = methods.ItemMethods()

        while True:
            items = item_methods.get_items()
            sorted_items = []
            while len(items) > 1:
                _right = randint(1, len(items) - 1)
                sorted_items.append(items[:_right])
                del items[:_right]

            choice(sorted_items).append(items[0])

            del items

            shop = ShopAPI()
            added = False

            for _items in sorted_items:
                try:
                    shop.add_items(_items)
                    added = True
                except exceptions.NotAvailable:
                    break

            if added:
                for item in sorted_items:
                    item_methods.decrease_item(item, item.count)

            sleep(10000)
