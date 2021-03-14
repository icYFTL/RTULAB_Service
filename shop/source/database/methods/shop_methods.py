from ..models import *
from . import session


class ShopMethods:
    def __init__(self):
        self.__session = session

    def add_shop(self, shop: Shop) -> Shop:
        self.__session.add(shop)
        self.__session.commit()

        return shop

    def get_slot_by_id(self, shop: Shop, slot_id: int) -> Slot:
        result = [x for x in self.__session.query(Slot).filter_by(shop_id=shop.id, id=slot_id)]
        if result:
            result = result[0]
        else:
            result = None

        return result

    def remove_shop(self, shop: Shop) -> None:
        self.__session.delete(shop)
        self.__session.commit()

    def get_shops(self, **kwargs) -> list:
        return [x for x in self.__session.query(Shop).filter_by(**kwargs)]