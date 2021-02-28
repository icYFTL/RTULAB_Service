from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .. import Base
from . import Item
from .base_model import BaseModel


class Purchase(Base, BaseModel):
    __tablename__ = 'purchases'

    id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(Integer, ForeignKey(Item.id), nullable=False)
    item = relationship('Item', backref='item')
    ts = Column(Integer, nullable=False)
    total = Column(Integer, nullable=False)

    def __init__(self, item_id: int, ts: int, total: int):
        self.item_id = item_id
        self.ts = ts
        self.total = total

    def __repr__(self):
        return f"<Purchase(id={self.id}, total={self.total})>"
