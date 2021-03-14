from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from .. import Base
from .base_model import BaseModel


class User(Base, BaseModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    # some other information
    purchases = relationship('Purchase', backref='purchases', uselist=True)

    def __init__(self, id=None):
        self.id = id

    def __repr__(self):
        return f"<User(id={self.id})>"
