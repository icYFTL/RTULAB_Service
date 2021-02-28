from ..models import *
from .. import Session


class ItemsMethods:
    def __init__(self):
        self.__session = Session()

    def add_new_item(self, item: Item) -> Item:
        self.__session.add(item)
        self.__session.commit()

        return item

    def get_item(self, **kwargs) -> Item:
        result = [x for x in self.__session.query(Item).filter_by(**kwargs)]
        return result[0] if result else None

    def remove_item(self, item: Item) -> None:
        self.__session.delete(item)
        self.__session.commit()
