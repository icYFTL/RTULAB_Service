from ..models import Slot
from . import session


class SlotMethods:
    def __init__(self):
        self.__session = session

    def add_slot(self, slot: Slot) -> Slot:
        self.__session.add(slot)
        self.__session.commit()

        return slot

    def remove_slot(self, slot: Slot) -> None:
        self.__session.delete(slot)
        self.__session.commit()

    def buy_slot(self, slot: Slot, count: int) -> bool:
        if slot.count >= abs(count):
            setattr(slot, 'count', slot.count - abs(count))
            self.__session.commit()
            return True
        return False

    def get_slots(self, **kwargs) -> list:
        return [x for x in self.__session.query(Slot).filter_by(**kwargs)]