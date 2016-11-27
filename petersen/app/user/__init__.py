import flask
from flask import request, abort, session
from petersen.app.base import app
from petersen.models import User, Connection, needs_db, Tag
from petersen.app.utils import is_connected, needs_logged_in
import bcrypt
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_, or_


@app.route('/user/new', methods=['POST'])
@needs_db
def new_user(db_session):
    data = request.get_json()

    if data is None:
        abort(400)

    if 'name' not in data:
        abort(400)
    if 'username' not in data:
        abort(400)
    if 'password' not in data:
        abort(400)

    # Validate fields

    user = User(
        name=data['name'],
        username=data['username'],
        password=bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    )

    try:
        db_session.add(user)
        db_session.commit()
    except IntegrityError:
        return flask.jsonify(**{
            'error': 'Username is already taken.'
        })

    session['user_id'] = user.user_id # Log them in

    return flask.jsonify(**{
        'user_id': user.user_id
    })


@app.route('/user/<int:user_id>', methods=['GET', 'POST'])
@needs_db
@needs_logged_in
def user_endpoint(db_session, user_id):
    requester = session['user_id']
    if request.method == 'GET':
        # Get info

        if requester == user_id or is_connected(db_session, user_id, requester):
            data = db_session.query(
                User
            ).filter(
                User.user_id == user_id
            )
            tags = db_session.query(Tag.tag) \
                .filter(Tag.user_id == user_id).all()

            if data.count() == 1:
                user = data.one()

                return flask.jsonify(**{
                    'name': user.name,
                    'username': user.username,
                    'tags': tags,
                })

    else:
        # Update info
        has_perms = False
        if requester == user_id:
            has_perms = True
        else:
            perms = db_session.query(
                User.is_admin
            ).filter(
                User.user_id == requester
            )

            if perms.count() == 1:
                if perms.one().is_admin:
                    has_perms = True

        if has_perms:
            data = db_session.query(
                User
            ).filter(
                User.user_id == user_id
            )

            if data.count() == 1:
                user = data.one()

                r = request.get_json()
                for k in r:
                    v = r[k]
                    if k == 'user_id': continue  # Can't change user id
                    if k == 'password':
                        # If it's a password, hash it
                        v = bcrypt.hashpw(v.encode('utf-8'), bcrypt.gensalt())
                    setattr(user, k, v)

                db_session.commit()

                return ('', 200)

    return flask.jsonify(**{
        'error': 'Invalid user'
    })


@app.route('/user/<int:user_id>/connect', methods=['POST', 'DELETE'])
@needs_db
@needs_logged_in
def connect_endpoint(db_session, user_id):
    me = session['user_id']
    if request.method == 'POST':
        is_pending = db_session.query(Connection).filter(
            Connection.sender_id == user_id,
            Connection.receiver_id == me,
            Connection.is_pending == True
        )
        if is_pending.count() == 1:
            is_pending.one().is_pending = False
            db_session.commit()
        else:
            req = Connection(
                sender_id=me,
                receiver_id=user_id
            )

            try:
                db_session.add(req)
                db_session.commit()
            except IntegrityError:
                return flask.jsonify(**{
                    'error': 'Already connected'
                })

    elif request.method == 'DELETE':
        con = db_session.query(Connection).filter(
            or_(
                and_(
                    Connection.sender_id == me,
                    Connection.receiver_id == user_id
                ),
                and_(
                    Connection.sender_id == user_id,
                    Connection.receiver_id == me
                )
            )
        )

        if con.count() == 1:
            con.delete()
            db_session.commit()
        else:
            return flask.jsonify(**{
                'error': 'Invalid user'
            })

    return ('', 200)


@app.route('/user/connections', methods=['GET'])
@needs_db
@needs_logged_in
def list_connections(db_session):
    me = session['user_id']

    conns = db_session.query(
        Connection.sender_id,
        Connection.receiver_id
    ).filter(
        or_(
            Connection.sender_id == me,
            Connection.receiver_id == me
        ),
        Connection.is_pending == False
    )

    resp = []
    for sender, receiver in conns:
        other = sender
        if sender == me: other = receiver
        resp.append(other)

    return flask.jsonify(**{
        'connections': resp
    })


@app.route('/user/connections/pending', methods=['GET'])
@needs_db
@needs_logged_in
def list_pending(db_session):
    me = session['user_id']

    conns = db_session.query(
        Connection.sender_id,
        Connection.receiver_id
    ).filter(
        or_(
            Connection.sender_id == me,
            Connection.receiver_id == me
        ),
        Connection.is_pending == True
    )

    resp = []
    for sender, receiver in conns:
        other = sender
        if sender == me: other = receiver
        resp.append(other)

    return flask.jsonify(**{
        'requests': resp
    })

