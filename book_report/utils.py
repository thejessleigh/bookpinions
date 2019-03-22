import os

from django.core.exceptions import ObjectDoesNotExist
from goodreads.client import GoodreadsClient

from book_report.users.models import User


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


def get_goodreads_client():
    gc = GoodreadsClient(os.environ["GOODREADS_KEY"], os.environ["GOODREADS_SECRET"])
