from sqlalchemy import Column, Integer, ForeignKey, String
from .. import Base

from source.database.models.shop import Shop
from source.database.models.user import User
from source.database.models.slot import Slot

from .base_model import BaseModel


class Transaction(Base, BaseModel):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id),nullable=False)
    shop_id = Column(Integer, ForeignKey(Shop.id), nullable=False)
    slot_id = Column(Integer, ForeignKey(Slot.id), nullable=False)
    count = Column(Integer, nullable=False)
    total = Column(Integer, nullable=False)
    ts = Column(Integer, nullable=False)
    method = Column(String, nullable=False)

    def __init__(self, user_id: int, shop_id: int, slot_id: int, count: int, total: int, ts: int, method: str):
        self.user_id = user_id
        self.shop_id = shop_id
        self.slot_id = slot_id
        self.count = count
        self.total = total
        self.ts = ts
        self.method = method.strip()

    def __repr__(self):
        return f"<Transaction(id={self.id}, shop_id={self.shop_id}, user_id={self.user_id})>"
