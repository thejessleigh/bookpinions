import datetime
import os
import webbrowser

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render, redirect
from goodreads.client import GoodreadsClient
from goodreads.session import GoodreadsSession


from book_report.models import User

gc = GoodreadsClient(os.environ["GOODREADS_KEY"], os.environ["GOODREADS_SECRET"])


def sign_in(request):
    if request.session.get("gid") is not None:
        user = User.objects.get(goodreads_user_id=request.session["gid"])
        gc.authenticate(
            access_token=user.access_token, access_token_secret=user.access_secret
        )
        redirect("/status")
    gc.session = GoodreadsSession(gc.client_key, gc.client_secret)
    url = gc.session.oauth_init()
    webbrowser.open(url)
    return redirect(url)


def gc_authenticate_callback(request):
    gc.session.oauth_finalize()
    print("HELLO")
    user = gc.user()
    print(user)
    if user is not None:
        request.session["logged_in"] = True
        request.session["gid"] = user.gid
        get_or_create_user(user)
    else:
        return render(request, "book_report/500.html")
    return render(request, "book_report/user_list.html", {"users": [user]})


def get_or_create_user(goodreads_user):
    try:
        user = User.objects.get(goodreads_user_id=goodreads_user.gid)
    except ObjectDoesNotExist:
        user = User(
            goodreads_user_id=goodreads_user.gid,
            name=goodreads_user.name,
            username=goodreads_user.user_name,
            access_token=gc.session.access_token,
            access_secret=gc.session.access_token_secret,
            visibility=0,
            created=datetime.datetime.utcnow(),
            updated=datetime.datetime.utcnow(),
        )
        user.save()
    return user


def user_list(request):
    # TODO: don't query for user if no session id. Throw bad login error if gid does not exist in db
    users = User.objects.filter(visibility=1).order_by("username")
    try:
        logged_in_user = User.objects.get(goodreads_user_id=request.session.get("gid"))
        if logged_in_user not in users:
            users.append(logged_in_user)
    except ObjectDoesNotExist:
        pass

    return render(request, "book_report/user_list.html", {"users": users})


def get_all_shelf_reviews_for_user(request, user_gid, shelf_name="read"):
    # TODO: might break out reviews vs users view functions into separate files
    if user_gid == request.session.get("gid"):
        visible = True
    else:
        try:
            user = User.objects.get(goodreads_user_id=user_gid)
            if user.visibility == 0:
                visible = False
            visible = True
        except ObjectDoesNotExist:
            visible = False

    if visible is False:
        raise Http404("User not found")

    reviews = gc.user(user_gid).per_shelf_reviews(shelf_name=shelf_name)

    return render(request, "book_report/user_shelf_reviews.html", {"reviews": reviews})
