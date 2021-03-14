from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from .. import Base
from .base_model import BaseModel


class Shop(Base, BaseModel):
    __tablename__ = 'shops'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    number = Column(String, nullable=False)

    slots = relationship('Slot', backref='slots', uselist=True)
    transactions = relationship('Transaction', backref='transactions', uselist=True)

    def __init__(self, name: str, address: str, number: int):
        self.name = name.strip()
        self.address = address.strip()
        self.number = number

    def __repr__(self):
        return f"<Shop(id={self.id}, name={self.name})>"
