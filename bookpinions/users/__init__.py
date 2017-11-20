import datetime
import time

from flask import session
from sqlalchemy import and_

from app import db, gc
from bookpinions.users.models import User

#TODO: Set up routes
#TODO: Break things out into routes and helpers in a separate file


def sign_in():
    gc.authenticate()
    user = gc.user()
    if gc.user() is not None:
        session['logged_in'] = True
        session['gid'] = user.gid
        get_or_create_user()
    else:
        # TODO: redirect unable to authorize - please try again
        return


def sign_out():
    session.clear()
    # TODO: redirect to home page
    return


def get_or_create_user():
    user = db.user.filter_by(goodreads_user_id=session['gid']).first()
    if user is None:
        gc_user = gc.user()
        user = User(
            goodreads_user_id=gc_user.gid,
            name=gc_user.name,
            created_time=datetime.datetime.now()
        )
        db.session.add(user)
        db.session.commit()
    return user


def get_user(user_gid):
    if user_gid == session['gid']:
        user = db.user.filter_by(goodreads_user_id=session['gid'])
    else:
        user = db.user.filter(and_(db.user.goodreads_user_id == session['gid']), db.user.visibility == 'public').first()
    return user


def get_all_shelf_reviews_for_logged_in_user(shelf_name='read'):
    # might try using other shelves in the future - keep this option open
    reviews_total = []
    total = 1
    while len(reviews_total) < total:
        reviews, total = gc.user().per_shelf_reviews()
        reviews_total.extend(reviews)
        # goodreads has a 1 call/s rate limit - respect that here
        time.sleep(1)

    return reviews_total
