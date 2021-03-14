from threading import Thread
from ..database import *
from random import choice, randint
from core import production, factory_state
from time import sleep


class Factory(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.state = 'offline'
        self.status = ''

    def run(self) -> None:
        item_methods = methods.ItemMethods()
        self.state = 'online'

        while True:
            if factory_state.isSet():
                self.state = 'offline'
                break

            category = choice(list(production))
            making_time = randint(1, 10)
            count = randint(1, 5)

            essence = choice(production[category])

            self.status = f'the {essence} is made for {making_time} seconds'
            sleep(making_time)

            item = item_methods.get_items(name=essence.lower())
            if not item:
                item = item_methods.add_item(models.Item(essence, category))
            else:
                item = item[0]

            print(item)

            item_methods.increase_item(item, count)

            self.status = 'cooldown for 30 seconds'

            sleep(30)




