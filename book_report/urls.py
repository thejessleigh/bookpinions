from django.urls import path

from book_report import views

urlpatterns = [
    path("", views.user_list, name="user_list"),
    path("signin", views.sign_in, name="sign_in"),
    path("callback", views.gc_authenticate_callback, name="callback"),
]
