import flask
from flask import request, abort
from petersen.app.base import app
from petersen.models import User, UserBadge, Tag, needs_db
from sqlalchemy import or_


@app.route('/users', methods=['GET'])
@needs_db
def user_filter(db_session):
    data = request.args

    if data is None:
        abort(400)

    filters = []

    for (k, v) in data.items():
        if k == 'name':
            filters.append(
                User.name.like("%{}%".format(v))
            )
        elif k == 'tags':
            filters.append(
                or_(
                    *[
                        Tag.tag == t
                        for t in v.split(',')
                    ]
                )
            )
        elif k == 'badges':
            filters.append(
                or_(
                    *[
                        UserBadge.badge_id == t
                        for t in v.split(',')
                    ]
                )
            )
        else:
            abort(400)

    peeps = db_session.query(
        User
    ).join(UserBadge, Tag).filter(
        *filters
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
