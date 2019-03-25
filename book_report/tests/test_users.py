import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.urls import resolve
from goodreads.user import GoodreadsUser
import mock
import pytest

from book_report.users.models import User
from book_report.users.views import (
    get_or_create_user,
    user_list,
    sign_in,
    sign_out,
    get_all_shelf_reviews_for_user,
)


class TestUsers:
    def create_user(self):
        return User(
            goodreads_user_id=5280,
            username="amilehigh",
            name="Millicent Denver",
            visibility=1,
            access_token="token",
            access_secret="secret",
            created=datetime.datetime.now(),
        )


class TestUserModel(TestUsers):
    def create_user(self):
        return User(
            goodreads_user_id=5280,
            username="amilehigh",
            name="Millicent Denver",
            visibility=1,
            access_token="token",
            access_secret="secret",
            created=datetime.datetime.now(),
        )

    def test_user_creation(self):
        user = self.create_user()
        assert type(user) is User
        assert str(user), "5280:Millicent Denver"


class TestUserUrlsCallCorrectFunctions(TestUsers):
    def test_user_list(self):
        endpoint = resolve("/users/")
        assert endpoint.func == user_list

    def test_sign_in(self):
        endpoint = resolve("/users/signin")
        assert endpoint.func == sign_in

    def test_sign_out(self):
        endpoint = resolve("/users/signout")
        assert endpoint.func == sign_out

    def test_get_shelf_reviews(self):
        endpoint = resolve("/users/user-reviews/5280")
        assert endpoint.func == get_all_shelf_reviews_for_user
        assert endpoint.kwargs["user_gid"] == 5280


class TestUserViews(TestUsers):
    def create_goodreads_user(self):
        user_dict = {"id": 5280, "name": "Millicent Denver", "user_name": "amilehigh"}
        return GoodreadsUser(user_dict, None)

    @mock.patch("book_report.users.views.User.objects")
    def test_get_or_create_user_for_existing_user(self, mock_user_objects):
        """
        Test get_or_create_user returns User object if user already exists in the database
        :param mock_user_objects:
        :return:
        """
        gr_user = self.create_goodreads_user()
        mock_user_objects.get.return_value = self.create_user()
        existing_user = get_or_create_user(gr_user, None)
        assert existing_user is not None
        assert type(existing_user) is User

    @mock.patch("book_report.users.views.User.objects")
    def test_get_or_create_user_for_new_user(self, mock_user_objects):
        """
        Test get_or_create_user returns newly created user if user is not found in the database
        :param mock_user_objects:
        :return:
        """
        gr_user = self.create_goodreads_user()
        mock_user_objects.get.side_effect = ObjectDoesNotExist
        mock_client = mock.Mock()
        mock_client.session.access_token = "access"
        mock_client.session.access_token_secret = "secret"
        with mock.patch("book_report.users.views.User.save"):
            new_user = get_or_create_user(gr_user, mock_client)
            assert new_user is not None
            assert type(new_user) is User
