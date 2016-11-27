from petersen.app.base import app
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    TIMESTAMP
)
from pytz import utc
from datetime import datetime as dt
from sqlalchemy.orm import sessionmaker
from petersen.models.base import Base
from functools import wraps
import json


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    name = Column(String)
    username = Column(String, unique=True)
    password = Column(String)
    is_admin = Column(Boolean, default=False)

    def to_json(self):
        return dict(
            user_id=self.user_id,
            name=self.name,
            is_admin=self.is_admin
        )


class Badge(Base):
    __tablename__ = 'badges'

    badge_id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    image_path = Column(String)


class UserBadge(Base):
    __tablename__ = 'user_badges'

    user_id = Column(Integer, ForeignKey(User.user_id), primary_key=True)
    badge_id = Column(Integer, ForeignKey(Badge.badge_id), primary_key=True)


class Connection(Base):
    __tablename__ = 'connections'

    sender_id = Column(Integer, ForeignKey(User.user_id), primary_key=True)
    receiver_id = Column(Integer, ForeignKey(User.user_id), primary_key=True)
    is_pending = Column(Boolean, default=True)


class Tag(Base):
    __tablename__ = 'tags'

    user_id = Column(Integer, ForeignKey(User.user_id), primary_key=True)
    tag = Column(String, primary_key=True)


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey(User.user_id))
    receiver_id = Column(Integer, ForeignKey(User.user_id))
    message = Column(String)
    sent_time = Column(TIMESTAMP(timezone=True), default=utc.localize(dt.now()))
    read = Column(Boolean, nullable=False, server_default='false', default=False)

    def to_json(self):
        return {
            'sender': self.sender_id,
            'reciever': self.receiver_id,
            'message': self.message,
            'sent_time': json.dumps(self.sent_time)
        }

engine = create_engine(app.config['db_url'], echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


def needs_db(func):
    @wraps(func)
    def f_wrapper(*args, **kwargs):
        db_session = Session()
        ret = func(db_session, *args, **kwargs)
        db_session.close()
        return ret
    return f_wrapper
