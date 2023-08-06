from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase, override_settings

from .utils import get_parameters, get_query_string, get_user


class TestUtils(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="john", password="doe")

    def get_request_with_token(self):
        return RequestFactory().get("/" + get_query_string(self.user))

    def test_get_parameters(self):
        self.assertEqual(list(get_parameters(self.user)), ["url_auth_token"])

    def test_get_query_string(self):
        self.assertIn("?url_auth_token=", get_query_string(self.user))

    def test_get_user(self):
        request = self.get_request_with_token()
        self.assertEqual(get_user(request), self.user)

    def test_get_user_no_token(self):
        request = RequestFactory().get("/")
        self.assertIsNone(get_user(request))

    def test_get_user_does_not_invalidate_tokens(self):
        request = self.get_request_with_token()
        self.assertEqual(get_user(request), self.user)
        self.assertEqual(get_user(request), self.user)

    @override_settings(SESAME_ONE_TIME=True)
    def test_get_user_invalidates_one_time_tokens(self):
        request = self.get_request_with_token()
        self.assertEqual(get_user(request), self.user)
        self.assertIsNone(get_user(request))

    def test_get_user_does_not_update_last_login(self):
        request = self.get_request_with_token()
        self.assertIsNone(self.user.last_login)
        self.assertEqual(get_user(request), self.user)
        self.user.refresh_from_db()
        self.assertIsNone(self.user.last_login)

    @override_settings(SESAME_ONE_TIME=True)
    def test_get_user_updates_last_login_for_one_time_tokens(self):
        request = self.get_request_with_token()
        self.assertIsNone(self.user.last_login)
        self.assertEqual(get_user(request), self.user)
        self.user.refresh_from_db()
        self.assertIsNotNone(self.user.last_login)

    def test_get_user_force_update_last_login(self):
        request = self.get_request_with_token()
        self.assertIsNone(self.user.last_login)
        self.assertEqual(get_user(request, update_last_login=True), self.user)
        self.user.refresh_from_db()
        self.assertIsNotNone(self.user.last_login)

    @override_settings(SESAME_ONE_TIME=True)
    def test_get_user_force_not_update_last_login(self):
        request = self.get_request_with_token()
        self.assertIsNone(self.user.last_login)
        self.assertEqual(get_user(request, update_last_login=False), self.user)
        self.user.refresh_from_db()
        self.assertIsNone(self.user.last_login)
