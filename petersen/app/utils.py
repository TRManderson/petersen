from petersen.models import Connection
from sqlalchemy import and_, or_
from functools import wraps
from flask import session, abort


def is_connected(db_session, user1, user2):
    connection = db_session.query(
        Connection.sender_id,
        Connection.receiver_id
    ).filter(
        or_(
            and_(
                Connection.sender_id == user1,
                Connection.receiver_id == user2
            ),
            and_(
                Connection.sender_id == user2,
                Connection.receiver_id == user1
            )
        ),
        Connection.is_pending == False
    )
    if connection.count() == 1:
        return True
    else:
        return False

def needs_logged_in(func):
    @wraps(func)
    def f_wrapper(*args, **kwargs):
        if 'user_id' not in session:
            abort(403)
        return func(*args, **kwargs)
    return f_wrapper
