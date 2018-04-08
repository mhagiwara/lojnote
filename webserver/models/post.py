from datetime import datetime
from webserver.models import Base

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, Text, DateTime


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    time_created = Column(DateTime, nullable=False)
    time_updated = Column(DateTime, nullable=False)
    body = Column(Text)

    def __repr__(self):
        return '<Post %s:%s>' % (self.id, str(self.body)[:80])


def add_post(session, user_id, body=None):
    post = Post(user_id=user_id,
                time_created=datetime.now(),
                time_updated=datetime.now(),
                body=body)
    session.add(post)
    session.commit()

    return post.id


def get_post(session, post_id):
    post = session.query(Post).filter(Post.id == post_id).first()
    return post
