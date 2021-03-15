from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from .. import Base
from source.database.models.user import User
from source.database.models.item import Item
from .base_model import BaseModel


class Purchase(Base, BaseModel):
    __tablename__ = 'purchases'

    id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(Integer, ForeignKey(Item.id), nullable=False)
    ts = Column(Integer, nullable=False)
    total = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey(User.id))
    method = Column(String, nullable=True)
    shop_id = Column(Integer, nullable=False)

    item = relationship('Item', backref='item')

    def __init__(self, item_id: int, ts: int, total: int, user_id: int, shop_id: int, method=None):
        self.item_id = item_id
        self.ts = ts
        self.total = total
        self.user_id = user_id
        self.shop_id = shop_id
        self.method = method

    def __repr__(self):
        return f"<Purchase(id={self.id}, total={self.total})>"
