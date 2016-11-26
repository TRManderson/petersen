import flask
from flask import request, abort, session
from petersen.app.base import app
from petersen.models import User, Connection, needs_db
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


@app.route('/user/<int:user_id>', methods=['GET'])
@needs_db
def get_user(db_session, user_id):
    data = db_session.query(
        User.name
    ).join(
        Connection
    ).filter(
        User.user_id == user_id,


    ).one()

    return flask.jsonify(**{
        'name': data.name
    })


@app.route('/debug/list_users', methods=['GET'])
def list_users():
    pass