from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_URL = 'mysql://root:jbopre@db/lojnote'

engine = create_engine(SQLALCHEMY_URL)
DBSession = sessionmaker(bind=engine)
