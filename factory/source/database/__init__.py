from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Engine = create_engine('sqlite:///test.db', echo=False, connect_args={'check_same_thread': False})
Base = declarative_base()
from .models import *


Base.metadata.create_all(Engine, checkfirst=True)

Session = sessionmaker(bind=Engine)
from .methods import *

__all__ = ['Session', 'Engine', 'models', 'methods']
