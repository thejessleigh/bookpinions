import operator

from django.http import Http404
from django.shortcuts import render

from book_report.utils import user_is_visible, get_goodreads_client


def controversial_opinions_report(request, user_gid, report_length=10):
    """
    Note: ratings with a review score of '0' will be discarded as they skew the results to books on your read shelf that haven't been rated.
    :param request:
    :param user_gid: goodreads id of the requested user
    :param report_length: how many books to include in the report
    :return:
    """
    gc = get_goodreads_client()
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


def most_loved_report(request, user_gid, report_length=10):
    """
    Create a report of the books a user loves more than the average goodreads user
    :param request:
    :param user_gid: goodreads id of the requested user
    :param report_length: how many books to include in the report
    :return:
    """
    pass
