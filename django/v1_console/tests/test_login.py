from config.error_codes import errors
from rest_framework.test import APITestCase

from django.conf import settings
from django.urls import reverse


class TestLogin(APITestCase):
    LOGIN_URL = reverse("auth_token")

    def setUp(self):
        is_cognito_config_not_set = len(settings.COGNITO_USER_POOL) < 10 or len(settings.COGNITO_CLIENT_ID) < 10
        if is_cognito_config_not_set:
            self.skipTest('Skip Cognito auth testcases since the settings are not set')

    def test_login_success(self):
        login_body = {
            "email": "tuanpx9184@co-well.com.vn",
            "login_password": "Admin@1234",
            "send_email_flag": True
        }
        login_response = self.client.post(self.LOGIN_URL, data=login_body)
        self.assertEqual(login_response.status_code, 200)
        data = login_response.data
        for key in ('token', 'token_expiration_date', 'refresh_token', 'terms_of_service_disagreement_flag'):
            self.assertTrue(key in data)

    def test_login_fail_invalid_credential(self):
        login_body = {
            "email": "tuanpx9184@co-well.com.vn",
            "login_password": "Admin@XXXX",  # wrong password
            "send_email_flag": True
        }
        login_response = self.client.post(self.LOGIN_URL, data=login_body)
        self.assertEqual(login_response.status_code, 401)
        data = login_response.data
        code = "LoginError"
        expect = {
            "status": {
                "code": code,
                "message": errors[code][1]
            }
        }
        self.assertEqual(data, expect)

    def test_login_invalid_param(self):
        login_body = {
            "email_email": "tuanpx9184@co-well.com.vn",  # wrong param
            "login_password": "Admin@XXXX",
            "send_email_flag": True
        }
        login_response = self.client.post(self.LOGIN_URL, data=login_body)
        self.assertEqual(login_response.status_code, 400)

    def test_first_login(self):
        # Todo: Need create account before run this test case
        login_body = {
            "email": "trananhkma@gmail.com",
            "login_password": "Admin@123",
            "send_email_flag": True
        }
        login_response = self.client.post(self.LOGIN_URL, data=login_body)
        self.assertEqual(login_response.status_code, 200)
        data = login_response.data
        code = "FirstLogin"
        expect = {
            "status": {
                "code": code,
                "message": errors[code][1]
            }
        }
        self.assertEqual(data, expect)
