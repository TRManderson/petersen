import flask
from petersen.app.base import app
from flask import request, session, abort
from petersen.models import User, needs_db
import bcrypt


@app.route('/login', methods=['POST'])
@needs_db
def login(db_session):
    data = request.get_json()
    if data is None:
        abort(400)

    if 'username' not in data:
        abort(400)

    if 'password' not in data:
        abort(400)

    results = db_session.query(
        User.user_id, User.password
    ).filter(
        User.username == data['username']
    )

    if results.count() == 1:
        user = results.one()
        if bcrypt.hashpw(data['password'].encode('utf-8'), user.password) == user.password:
            session['user_id'] = user.user_id
            return flask.jsonify(**{
                'user_id': user.user_id
            })

    return flask.jsonify(**{
        'error': 'Invalid username/password combination'
    })


@app.route('/logout', methods=['POST'])
def logout():
    if 'user_id' not in session:
        return flask.jsonify(**{
            'error': 'Not logged in'
        })

    session.pop('user_id', None)

    return ('', 200)


@app.route('/logged_in', methods=['GET'])
def logged_in():
    return flask.jsonify(**{
        'user_id': session.get('user_id', -1)
    })

