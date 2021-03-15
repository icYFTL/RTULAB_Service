from sqlalchemy import Column, String, Integer
from .. import Base
from .base_model import BaseModel


class Item(Base, BaseModel):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=True)
    count = Column(Integer, default=0)

    def __init__(self, name: str, category: str, count=0):
        self.name = name.strip()
        self.category = category.strip()
        self.count = count

    def __repr__(self):
        return f"<Item(id={self.id}, name={self.name})>"
