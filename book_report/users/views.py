import datetime
import webbrowser

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render, redirect
from goodreads.session import GoodreadsSession

from book_report.users.models import User
from book_report.utils import user_is_visible, get_goodreads_client


def sign_in(request):
    gc = get_goodreads_client()
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


def sign_out(request):
    del request.session["gid"]
    return redirect("")


def gc_authenticate_callback(request):
    gc = get_goodreads_client()
    gc.session.oauth_finalize()
    user = gc.user()
    if user is not None:
        request.session["logged_in"] = True
        request.session["gid"] = user.gid
        get_or_create_user(user, gc)
    else:
        return render(request, "book_report/500.html")
    return render(request, "book_report/user_list.html", {"users": [user]})


def get_or_create_user(goodreads_user, goodreads_client):
    try:
        user = User.objects.get(goodreads_user_id=goodreads_user.gid)
    except ObjectDoesNotExist:
        user = User(
            goodreads_user_id=goodreads_user.gid,
            name=goodreads_user.name,
            username=goodreads_user.user_name,
            access_token=goodreads_client.session.access_token,
            access_secret=goodreads_client.session.access_token_secret,
            visibility=1,
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
    gc = get_goodreads_client()
    if not user_is_visible(request.session.get("gid"), user_gid):
        raise Http404("User not found")

    reviews = gc.user(user_gid).per_shelf_reviews(shelf_name=shelf_name)

    return render(request, "book_report/user_shelf_reviews.html", {"reviews": reviews})
