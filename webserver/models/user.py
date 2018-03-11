from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import Integer, String, Text, DateTime, Boolean
from webserver.models import Base


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


def get_user(session, user_id):
    user = session.query(User).filter(User.id == user_id).first()
    return user


def add_user(session, alias=None, email=None, password=None):
    user = User(alias=alias,
                email=email,
                password=password,
                time_created=datetime.now(),
                active=True)
    session.add(user)
    session.commit()

    return user.id


def inactivate_user(session, user_id):
    pass


def modify_user(session, user_id):
    pass
