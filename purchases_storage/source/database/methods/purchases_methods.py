from ..models import Purchase
from .. import Session


class PurchasesMethods:
    def __init__(self):
        self.__session = Session()

    def add_purchase(self, purchase: Purchase) -> Purchase:
        self.__session.add(purchase)
        self.__session.commit()

        return purchase

    def get_purchases(self, **kwargs) -> list:
        result = [x for x in self.__session.query(Purchase).filter_by(**kwargs)]
        return result if result else None

    def remove_purchase(self, purchase: Purchase) -> None:
        self.__session.delete(purchase)
        self.__session.commit()
