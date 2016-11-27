import flask
from flask import request, abort
from petersen.app.base import app
from petersen.models import User, needs_db


@app.route('/users', methods=['GET'])
@needs_db
def new_user(db_session):
    data = request.args

    if data is None:
        abort(400)

    peeps = db_session.query(
        User
    ).filter(
        *[
            getattr(User, k) == v
            for (k, v) in data.items()
        ]
    )

    resp = [
        {
            p.to_json()
        }
        for p in peeps
    ]

    return flask.jsonify(**{
        'users': resp
    })
