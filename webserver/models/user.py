from sqlalchemy import create_engine, Column
from sqlalchemy import Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_URL = 'mysql://root:jbopre@db/lojnote'

engine = create_engine(SQLALCHEMY_URL)
DBSession = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    alias = Column(String(255), nullable=False)
    email = Column(String(256), nullable=False)
    password = Column(String(256), nullable=False)
    time_created = Column(DateTime, nullable=False)
    active = Column(Boolean, nullable=False)
    profile = Column(Text)

    def __repr__(self):
        return '<User %s:%s>' % (self.id, self.alias)
