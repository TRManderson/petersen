import flask
from flask import request, session, abort
from petersen.models import needs_db, Message
from petersen.app.base import app
from petersen.app.utils import is_connected, needs_logged_in


@app.route('/message/send/<int:user_id>', methods=['POST'])
@needs_db
@needs_logged_in
def send_message(db_session, user_id):
    data = request.get_json()
    if 'message' in data:
        sender = session['user_id']
        if is_connected(db_session, user_id, sender):
            msg = Message(
                sender_id=sender,
                receiver_id=user_id,
                message=data['message']
            )

            db_session.add(msg)
            db_session.commit()

            return ('', 200)

    return flask.jsonify(**{
        'error': 'Invalid user/message'
    })


@app.route('/message/recv/<int:user_id>', methods=['GET'])
@needs_db
@needs_logged_in
def recv_message(db_session, user_id):
    me = session['user_id']
    if is_connected(db_session, user_id, sender):
        msgs = db_session.query(
            Message.message
        ).filter(
            Message.sender_id == user_id,
            Message.receiver_id == me
        )

        resp = [
            {
                'msg': m
            }
            for m in msgs
        ]

        return flask.jsonify(**{
            'messages': resp
        })

    return flask.jsonify(**{
        'error': 'Invalid user'
    })

