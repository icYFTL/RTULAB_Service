from sqlalchemy import Column, String, Integer, ForeignKey
from .. import Base
from .base_model import BaseModel
from source.database.models.shop import Shop


class Slot(Base, BaseModel):
    __tablename__ = 'slots'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Integer, nullable=False)
    category = Column(String, nullable=True)
    count = Column(Integer, nullable=False)
    shop_id = Column(Integer, ForeignKey(Shop.id))

    def __init__(self, name: str, description: str, price: int, category: str, count: int, shop_id: int):
        self.name = name.strip()
        self.description = description.strip()
        self.price = abs(price)
        self.category = category.strip()
        self.count = abs(count)
        self.shop_id = shop_id


    def __repr__(self):
        return f"<Slot(id={self.id}, name={self.name})>"
