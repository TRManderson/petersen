import flask
from flask import request, abort
from petersen.app.base import app
from petersen.models import User, needs_db


@app.route('/user/new', methods=['POST'])
@needs_db
def new_user(db_session):
    data = request.get_json()

    if 'name' not in data:
        abort(400)

    user = User(name=data['name'])

    db_session.add(user)
    db_session.commit()

    return flask.jsonify(**{
        'user_id': user.user_id
    })


@app.route('/debug/list_users', methods=['GET'])
def list_users():
    pass