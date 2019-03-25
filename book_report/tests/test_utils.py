import datetime

import mock

from book_report.users.models import User
from book_report.utils import user_is_visible


@mock.patch("book_report.utils.User.objects")
class TestUserVisibility:
    def create_user(self, visibility):
        return User(
            goodreads_user_id=5280,
            username="amilehigh",
            name="Millicent Denver",
            visibility=visibility,
            access_token="token",
            access_secret="secret",
            created=datetime.datetime.now(),
        )

    def test_user_visibility_1(self, mock_user_objects):
        mock_user_objects.get.return_value = self.create_user(visibility=1)
        session_user_id = 50  # not the requested user
        assert user_is_visible(session_user_id, 5280)

    def test_user_visibility_0(self, mock_user_objects):
        mock_user_objects.get.return_value = self.create_user(visibility=0)
        session_user_id = 50  # is the requested user
        assert not user_is_visible(session_user_id, 5280)

    def test_logged_in_user_is_visible_to_self_even_with_visibility_0(
        self, mock_user_objects
    ):
        mock_user_objects.get.return_value = self.create_user(visibility=0)
        session_user_id = 5280
        assert user_is_visible(session_user_id, 5280)
