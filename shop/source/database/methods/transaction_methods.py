from ..models import Transaction
from . import session


class TransactionMethods:
    def __init__(self):
        self.__session = session

    def add_transaction(self, transaction: Transaction) -> Transaction:
        self.__session.add(transaction)
        self.__session.commit()

        return transaction

    def remove_transaction(self, transaction: Transaction) -> None:
        raise NotImplemented  # Everyone have no rights to remove transactions

    def get_transactions(self, **kwargs) -> list:
        return [x for x in self.__session.query(Transaction).filter_by(**kwargs)]