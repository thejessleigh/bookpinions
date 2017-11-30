import datetime

from flask import session

from .models import User


def get_user(user_gid):
    if user_gid == session.get('gid'):
        user = User.query.filter_by(goodreads_user_id=session.get('gid'))
    else:
        user = User.query.filter_by(goodreads_user_id=user_gid).first()
    if user is None:
        user = User(name="None", username="None", access_token="None", access_secret="None", created_time=datetime.datetime.now(), goodreads_user_id=0)

    return user
