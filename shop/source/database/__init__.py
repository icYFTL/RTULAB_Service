from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core import db_config

conn_str = 'postgresql+psycopg2://{username}:{password}@{host}/{db}'.format(
    username=db_config['user'],
    password=db_config['password'],
    host=db_config['host'],
    db=db_config['db']
)

Engine = create_engine(conn_str, echo=False)
Base = declarative_base()
from .models import *


Base.metadata.create_all(Engine, checkfirst=True)

Session = sessionmaker(bind=Engine)
from .methods import *

__all__ = ['Session', 'Engine', 'models', 'methods']
