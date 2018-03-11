from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


SQLALCHEMY_URL = 'mysql://root:jbopre@db/lojnote'

engine = create_engine(SQLALCHEMY_URL)
session_maker = sessionmaker(bind=engine)
Base = declarative_base()


@contextmanager
def start_session():
    session = session_maker()
    yield session
    session.close()
