from ..models import Item
from . import session


class ItemMethods:
    def __init__(self):
        self.__session = session
        self.__session.begin_nested()

    def add_item(self, item: Item) -> Item:
        self.__session.add(item)
        self.__session.commit()

        return item

    def remove_item(self, item: Item) -> None:
        raise NotImplemented

    def get_items(self, **kwargs) -> list:
        return [x for x in self.__session.query(Item).filter_by(**kwargs)]

    def increase_item(self, item: Item, value: int) -> None:
        item.count += value
        self.__session.commit()

    def decrease_item(self, item: Item, value: int) -> None:
        if (item.count - value) > 0:
            item.count -= value

        self.__session.commit()

    def clear_item(self, item: Item) -> None:
        item.count = 0
        self.__session.commit()
