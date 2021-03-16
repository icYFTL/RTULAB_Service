from threading import Thread, Lock
from ..database import *
from random import choice, randint
from core import production
from time import sleep
from datetime import datetime, timedelta


class Factory(Thread):
    def __init__(self, category: str, delay=30):
        Thread.__init__(self)
        self.status = ''
        self.lock = Lock()
        self.delay = delay
        self.category = category
        self.defected = 0
        self.session_start = datetime.now().timestamp()

    def run(self) -> None:
        item_methods = methods.ItemMethods()

        while True:
            if self.lock.locked():
                self.status = 'locked'
                self.lock.acquire()

            if datetime.now().timestamp() - self.session_start > 86400:
                self.defected = 0
                self.session_start = datetime.now().timestamp()

            making_time = randint(1, 10)
            count = randint(1, 5)

            essence = choice(production[self.category])

            self.status = f'the {essence} will made for {making_time} seconds'
            sleep(making_time)

            try:
                item = item_methods.get_items(name=essence.lower())

                if not item:
                    item = item_methods.add_item(models.Item(essence, self.category))
                else:
                    item = item[0]

                item_methods.increase_item(item, count)
            except:  # defected items
                self.status = f'sleep for {self.delay} seconds'
                self.defected += 1
                sleep(self.delay)
                continue

            self.status = f'sleep for {self.delay} seconds'

            sleep(self.delay)
