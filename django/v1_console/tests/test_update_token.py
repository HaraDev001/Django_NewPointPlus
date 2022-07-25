from rest_framework.test import APITestCase

from django.conf import settings
from django.urls import reverse


class UpdateTokenTestCase(APITestCase):
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
        self.refresh_token = data['refresh_token']

    def test_update_token_success(self):
        update_token_body = {
            "refresh_token": self.refresh_token
        }
        update_token_response = self.client.put(self.URL_AUTHENTICATION, data=update_token_body)
        self.assertEqual(update_token_response.status_code, 200)
        data = update_token_response.data
        for key in ('token', 'token_expiration_date', 'terms_of_service_disagreement_flag'):
            self.assertTrue(key in data)

    def test_update_refresh_token_invalid(self):
        body_invalid_refresh_token = {
            "refresh_token": "XXXXXXXXXXXXXXXX"
        }
        update_token_response = self.client.put(self.URL_AUTHENTICATION, data=body_invalid_refresh_token)
        self.assertEqual(update_token_response.status_code, 401)
        data = update_token_response.data
        expect = {
            "status": {
                "code": "TokenAuthenticationError",
                "message": ""
            }
        }
        self.assertEqual(data, expect)

    def test_update_token_none_pram(self):
        body_none_param = {}
        update_token_response = self.client.put(self.URL_AUTHENTICATION, data=body_none_param)
        self.assertEqual(update_token_response.status_code, 400)
