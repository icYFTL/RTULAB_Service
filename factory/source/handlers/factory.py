from threading import Thread, Lock
from ..database import *
from random import choice, randint
from core import production
from time import sleep


class Factory(Thread):
    def __init__(self, category: str):
        Thread.__init__(self)
        self.state = 'offline'
        self.status = ''
        self.lock = Lock()
        self.delay = 30
        self.category = category

    def run(self) -> None:
        item_methods = methods.ItemMethods()
        self.state = 'online'

        while True:
            if self.lock.locked():
                self.status = 'locked'
                self.lock.acquire()

            making_time = randint(1, 10)
            count = randint(1, 5)

            essence = choice(production[self.category])

            self.status = f'the {essence} will made for {making_time} seconds'
            sleep(making_time)

            item = item_methods.get_items(name=essence.lower())
            if not item:
                item = item_methods.add_item(models.Item(essence, self.category))
            else:
                item = item[0]

            item_methods.increase_item(item, count)
            self.status = f'sleep for {self.delay} seconds'

            sleep(self.delay)
