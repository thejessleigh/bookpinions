import datetime
import operator
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
    """
    A user can only see a complete list of their own reviews
    :param request:
    :param user_gid:
    :param shelf_name:
    :return:
    """
    # TODO: might break out reviews vs users view functions into separate files
    if not user_is_visible(request.session.get("gid"), user_gid):
        raise Http404("User not found")

    reviews = gc.user(user_gid).per_shelf_reviews(shelf_name=shelf_name)

    return render(request, "book_report/user_shelf_reviews.html", {"reviews": reviews})


def identify_controversial_opinions(request, user_gid, report_length=20):
    """
    Note: ratings with a review score of '0' will be discarded as they skew the results to books on your read shelf that haven't been rated.
    :param request:
    :param user_gid:
    :param report_length:
    :return:
    """
    if not user_is_visible(request.session.get("gid"), user_gid):
        raise Http404("User not found")

    reviews = gc.user(user_gid).per_shelf_reviews(shelf_name="read")

    diffed_reviews = []

    for review in reviews:
        if review.rating == "0":
            continue
        average_score = review.book["average_rating"]
        diff = abs(float(average_score) - float(review.rating))
        diffed_reviews.append((diff, review))

    diffed_reviews.sort(key=operator.itemgetter(0), reverse=True)
    print(diffed_reviews)
    return render(
        request,
        "book_report/user_opinions_report.html",
        {"reviews": [r[1] for r in diffed_reviews][:report_length]},
    )


def user_is_visible(session_user_id, user_gid):
    """
    Helper function that determines if a requested user is visible to the logged in user.
    :param session_user_id:
    :param user_gid:
    :return:
    """
    if user_gid == session_user_id:
        visible = True
    else:
        try:
            user = User.objects.get(goodreads_user_id=user_gid)
            if user.visibility == 0:
                visible = False
            else:
                visible = True
        except ObjectDoesNotExist:
            visible = False

    return visible
