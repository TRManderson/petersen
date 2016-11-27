import flask
from petersen.app.utils import needs_admin
from petersen.models import needs_db, Connection
from petersen.app.base import app
from sqlalchemy.exc import IntegrityError


@app.route('/admin/connect/<int:user1>/<int:user2>')
@needs_db
@needs_admin
def connect_users(db_session, user1, user2):
    conn = Connection(
        sender_id=user1,
        reciever_id=user2,
        is_pending=False
    )

    try:
        db_session.add(conn)
        db_session.commit()
    except IntegrityError:
        return flask.jsonify(**{
            'error': 'Invalid users to connect'
        })

    return ('', 200)