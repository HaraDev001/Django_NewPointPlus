from rest_framework.test import APITestCase

from django.conf import settings
from django.urls import reverse


class RevokeTokenTestCase(APITestCase):
    URL_AUTHENTICATION = reverse("auth_token")

    def setUp(self) -> None:
        is_cognito_config_not_set = len(settings.COGNITO_USER_POOL) < 10 or len(settings.COGNITO_CLIENT_ID) < 10
        if is_cognito_config_not_set:
            self.skipTest('Skip Cognito auth testcases since the settings are not set')

        login_body = {
            "email": "tuanpx9184@co-well.com.vn",
            "login_password": "Admin@1234",
            "send_email_flag": True
        }
        login_response = self.client.post(self.URL_AUTHENTICATION, data=login_body)
        self.assertEqual(login_response.status_code, 200)
        data = login_response.data
        self.token = data['token']
        self.refresh_token = data['refresh_token']

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

    def tearDown(self) -> None:
        self.client.credentials()

    def test_revoke_token_success(self):
        revoke_token_body = {
            "refresh_token": self.refresh_token
        }
        revoke_token_response = self.client.delete(self.URL_AUTHENTICATION, data=revoke_token_body)
        self.assertEqual(revoke_token_response.status_code, 200)

    def test_revoke_token_invalid(self):
        revoke_token_body = {
            "refresh_token": "xxxxxxxxxxxxxx"
        }
        revoke_token_response = self.client.delete(self.URL_AUTHENTICATION, data=revoke_token_body)
        self.assertEqual(revoke_token_response.status_code, 200)

    def test_revoke_token_none_pram(self):
        body_none_param = {}
        revoke_token_response = self.client.delete(self.URL_AUTHENTICATION, data=body_none_param)
        self.assertEqual(revoke_token_response.status_code, 400)

    def test_has_not_permission(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + "xxxxx")
        revoke_token_body = {
            "refresh_token": self.refresh_token
        }
        revoke_token_response = self.client.delete(self.URL_AUTHENTICATION, data=revoke_token_body)
        self.assertEqual(revoke_token_response.status_code, 401)
