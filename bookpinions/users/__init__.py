import datetime
import json
import os
import time
import webbrowser

from flask import Blueprint, session, request, redirect, render_template
from goodreads.client import GoodreadsClient
from goodreads.session import GoodreadsSession
from sqlalchemy import and_

from bookpinions.templates import template_env
from bookpinions.users import views
from bookpinions.users.models import User
from utils import db

# TODO: Break things out into routes and helpers in a separate file

user_blueprint = Blueprint('user', __name__)

gc = GoodreadsClient(os.environ['GOODREADS_KEY'], os.environ['GOODREADS_SECRET'])


@user_blueprint.route('/sign-in', methods=['POST'])
def sign_in():
    if session.get('gid') is not None:
        user = User.query.get(session['gid'])
        gc.authenticate(access_token=user.access_token, access_token_secret=user.access_secret)
        redirect('/status')
    gc.session = GoodreadsSession(gc.client_key, gc.client_secret)
    url = gc.session.oauth_init()
    webbrowser.open(url)
    return redirect(url)


@user_blueprint.route('/callback', methods=['GET'])
def callback():
    gc.session.oauth_finalize()

    user = gc.user()
    if gc.user() is not None:
        session['logged_in'] = True
        session['gid'] = user.gid
        get_or_create_user(gc)
    else:
        return json.dumps({"status": 500})
    user = User.query.filter_by(goodreads_user_id=session.get('gid')).first()
    return json.dumps({"status": 201, "user": user.username})


@user_blueprint.route('/sign-out', methods=['POST'])
def sign_out():
    session.clear()
    # TODO: redirect to home page
    return redirect('/status')


def get_or_create_user(goodreads_client):
    user = User.query.filter_by(goodreads_user_id=session.get('gid')).first()
    if user is None:
        gc_user = goodreads_client.user()
        user = User(
            goodreads_user_id=gc_user.gid,
            name=gc_user.name,
            created_time=datetime.datetime.now(),
            username=gc_user.user_name,
            access_token=gc.session.access_token,
            access_secret=gc.session.access_token_secret
        )
        db.session.add(user)
        db.session.commit()
    return user


@user_blueprint.route('/<int:user_gid>', methods=['GET'])
def show_user(user_gid):
    user = views.get_user(user_gid)

    return render_template(template_env.get_template('show_user.html'), user=user)


@user_blueprint.route('/<int:user_gid>/reviews/<string:shelf_name>', methods=['GET'])
def get_all_shelf_reviews_for_user(user_gid, shelf_name):
    # TODO: this might not belong in the users controller
    if user_gid == session['gid']:
        visible = True
    else:
        user = db.user.filter(and_(db.user.goodreads_user_id == session.get('gid')), db.user.visibility == 'public').first()
        visible = True if user is not None else False

    if visible is False:
        return json.dumps({"status": 404, "message": "User not found"})
    reviews_total = []
    total = 1
    while len(reviews_total) < total:
        reviews, total = gc.user(user_gid).per_shelf_reviews(shelf_name)
        reviews_total.extend(reviews)

        # goodreads has a 1 call/s rate limit - respect that here
        time.sleep(1)

    return json.dumps({"reviews": reviews_total, "total": total, "status": 200})
