import requests
from config.exceptions import GenericException

from django.conf import settings
from django.test import TestCase

from ..email_utility import MailClient


class TestEmailUtility(TestCase):

    def setUp(self):
        is_todoku_config_not_set = len(settings.TODOKU_CLIENT_ID) < 10 or len(settings.TODOKU_CLIENT_SECRET) < 10
        if is_todoku_config_not_set:
            self.skipTest('Skip TODOKU email service testcases since the settings are not set')

        self.sender = MailClient(
            send_email_url=settings.TODOKU_SEND_EMAIL_URL,
            client_id=settings.TODOKU_CLIENT_ID,
            client_secret=settings.TODOKU_CLIENT_SECRET,
        )

    def test_send_email(self):
        """ Test case send email successfully """

        response = self.sender.send_raw_email(
            subject="Test",
            source="example@gmail.com",
            destinations=["receiver@gmail.com"],
            raw_message="Test send mail"
        )
        self.assertEqual(response.status_code, 200)

    def test_an_html_message(self):
        """ Test send an HTML message """

        response = self.sender.send_raw_email(
            subject="Test send an HTML message",
            source="example@gmail.com",
            destinations=["receiver@gmail.com"],
            raw_message="Test send mail",
            html_message="<h1>Test send an HTML message</h1>"
        )
        self.assertEqual(response.status_code, 200)

    def test_send_email_in_japanese(self):
        """ Check to send messages in Japanese """

        response = self.sender.send_raw_email(
            subject="Test send an HTML message",
            source="example@gmail.com",
            destinations=["receiver@gmail.com"],
            raw_message="日本語でメッセージを送信するためにチェックしてください",
        )
        self.assertEqual(response.status_code, 200)

    def test_authentication(self):
        """ Test successful authentication case """

        access_token = self.sender.get_access_token()
        self.assertIsInstance(access_token, str)
        self.assertGreater(len(access_token), 0)

    def test_authentication_fail(self):
        """ Test the authentication failed case """

        with self.assertRaises(requests.exceptions.RequestException):
            self.sender.get_access_token(
                auth_token_url=settings.TODOKU_SEND_EMAIL_URL
            )

    def test_connection_fail(self):
        """ Test the connection failure case """

        with self.assertRaises(GenericException):
            fake_sender = MailClient(
                send_email_url=settings.TODOKU_SEND_EMAIL_URL + "fake",
                client_id=settings.TODOKU_CLIENT_ID,
                client_secret=settings.TODOKU_CLIENT_SECRET,
            )
            fake_sender.send_raw_email(
                subject="Test",
                source="example@gmail.com",
                destinations=["receiver@gmail.com"],
                raw_message="Test send mail"
            )
