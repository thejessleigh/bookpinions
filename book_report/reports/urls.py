from django.urls import path

from book_report.reports import views

urlpatterns = [
    path(
        "opinion/<int:user_gid>",
        views.controversial_opinions_report,
        name="opinion_report",
    ),
    path("loved/<int:user_gid>", views.most_loved_report, name="loved-report"),
]
