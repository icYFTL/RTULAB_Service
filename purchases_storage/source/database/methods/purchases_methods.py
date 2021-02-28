from ..models import *
from .. import Session


class PurchasesMethods:
    def __init__(self):
        self.__session = Session()

    def add_new_purchase(self, purchase: Purchase) -> Purchase:
        self.__session.add(purchase)
        self.__session.commit()

        return purchase

    def get_purchase(self, **kwargs) -> Purchase:
        result = [x for x in self.__session.query(Purchase).filter_by(**kwargs)]
        return result[0] if result else None

    def remove_purchase(self, purchase: Purchase) -> None:
        self.__session.delete(purchase)
        self.__session.commit()
