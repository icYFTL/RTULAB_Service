from sqlalchemy import Column, String, Integer
from .. import Base
from .base_model import BaseModel


class Item(Base, BaseModel):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(collation='nocase'), nullable=False)
    category = Column(String(collation='nocase'), nullable=True)

    def __init__(self, name: str, category=None):
        self.name = name.strip()
        self.category = category

    def __repr__(self):
        return f"<Item(id={self.id}, name={self.name})>"
