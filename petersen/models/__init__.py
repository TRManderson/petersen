from petersen.app.base import app
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey
)
from sqlalchemy.orm import sessionmaker
from petersen.models.base import Base


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    name = Column(String)


class Badge(Base):
    __tablename__ = 'badges'

    badge_id = Column(Integer, primary_key=True)
    name = Column(String)
    image_path = Column(String)


class UserBadge(Base):
    __tablename__ = 'user_badges'

    user_id = Column(Integer, ForeignKey(User.user_id), primary_key=True)
    badge_id = Column(Integer, ForeignKey(Badge.badge_id), primary_key=True)


class Connection(Base):
    __tablename__ = 'connections'

    sender_id = Column(Integer, ForeignKey(User.user_id), primary_key=True)
    receiver_id = Column(Integer, ForeignKey(User.user_id), primary_key=True)
    is_pending = Column(Boolean)


class Tag(Base):
    __tablename__ = 'tags'

    user_id = Column(Integer, ForeignKey(User.user_id), primary_key=True)
    tag = Column(String, primary_key=True)


class Messages(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey(User.user_id))
    receiver_id = Column(Integer, ForeignKey(User.user_id))
    message = Column(String)

engine = create_engine(app.config['db_url'], echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


def needs_db(func):
    def f_wrapper(*args, **kwargs):
        db_session = Session()
        ret = func(db_session, *args, **kwargs)
        db_session.close()
        return ret
    return f_wrapper
