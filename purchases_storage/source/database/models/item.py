from sqlalchemy import Column, String, Integer
from .. import Base
from .base_model import BaseModel


class Item(Base, BaseModel):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(collation='nocase'), nullable=False)

    def __init__(self, name: str):
        self.name = name.strip()

    def __repr__(self):
        return f"<Item(id={self.id}, name={self.name})>"
