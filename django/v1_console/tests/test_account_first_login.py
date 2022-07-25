from config.error_codes import errors
from rest_framework.test import APITestCase
from v1_console.utils import issue_token

from django.conf import settings
from django.urls import reverse


class InitialPasswordTestCase(APITestCase):

    URL_INIT_PWD = reverse("account_set_password")

    def setUp(self) -> None:
        is_cognito_config_not_set = len(settings.COGNITO_USER_POOL) < 10 or len(settings.COGNITO_CLIENT_ID) < 10
        if is_cognito_config_not_set:
            self.skipTest('Skip Cognito auth testcases since the settings are not set')

        self.email = "trungtdd7298@co-well.com.vn"
        self.tmp_password = "Admin@123"
        self.init_password = "123qweQWE"

        try:
            self.create_test_account()
        except settings.COGNITO_CLIENT.exceptions.UsernameExistsException:
            self.remove_test_account()
            self.create_test_account()

        self.cognito_response = issue_token(username=self.email, password=self.tmp_password)
        self.session = self.cognito_response['Session']

    def tearDown(self) -> None:
        self.remove_test_account()

    def create_test_account(self):
        settings.COGNITO_CLIENT.admin_create_user(
            UserPoolId=settings.COGNITO_USER_POOL,
            Username=self.email,
            TemporaryPassword=self.tmp_password
        )

    def remove_test_account(self):
        settings.COGNITO_CLIENT.admin_delete_user(
            UserPoolId=settings.COGNITO_USER_POOL,
            Username=self.email
        )

    def test_set_password_fail_with_invalid_request_email_param(self):
        body_invalid_email_param = {
            "email_email": self.email,
            "login_password": self.init_password,
            "session": self.session
        }

        resp = self.client.put(self.URL_INIT_PWD, data=body_invalid_email_param)
        self.assertEqual(resp.status_code, 400)

    def test_set_password_fail_with_invalid_request_session_param(self):
        body_invalid_session_param = {
            "email": self.email,
            "login_password": self.init_password,
            "session_session": self.session
        }

        resp = self.client.put(self.URL_INIT_PWD, data=body_invalid_session_param)
        self.assertEqual(resp.status_code, 400)

    def test_set_password_fail_with_invalid_session(self):
        invalid_session = self.session + "str_append"
        body_invalid_session = {
            "email": self.email,
            "login_password": self.init_password,
            "session": invalid_session
        }

        error_code = "TokenAuthenticationError"
        expect = {
            "status": {
                "code": error_code,
                "message": errors[error_code][1]
            }
        }

        resp = self.client.put(self.URL_INIT_PWD, data=body_invalid_session)
        self.assertEqual(resp.status_code, 401)
        data = resp.data
        self.assertEqual(data, expect)

    def test_set_password_fail_with_invalid_credential(self):
        invalid_credential = "fake_" + self.email
        body_invalid_credential = {
            "email": invalid_credential,
            "login_password": self.init_password,
            "session": self.session
        }
        error_code = "TokenAuthenticationError"
        expect = {
            "status": {
                "code": error_code,
                "message": errors[error_code][1]
            }
        }

        resp = self.client.put(self.URL_INIT_PWD, data=body_invalid_credential)
        self.assertEqual(resp.status_code, 401)
        data = resp.data
        self.assertEqual(data, expect)

    def test_set_password_successfully(self):
        body_request = {
            "email": self.email,
            "login_password": self.init_password,
            "session": self.session
        }

        resp = self.client.put(self.URL_INIT_PWD, data=body_request)
        self.assertEqual(resp.status_code, 200)
