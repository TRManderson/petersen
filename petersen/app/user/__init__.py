import flask
from flask import request, abort, session
from petersen.app.base import app
from petersen.models import User, Connection, needs_db
from petersen.app.utils import is_connected, needs_logged_in
import bcrypt
from sqlalchemy.exc import IntegrityError


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
                User.name
            ).filter(
                User.user_id == user_id
            )

            if data.count() == 1:
                user = data.one()

                return flask.jsonify(**{
                    'name': user.name
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
