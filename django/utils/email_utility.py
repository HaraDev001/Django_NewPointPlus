import logging

import requests
from config.exceptions import GenericException
from config.logging import ADMIN
from requests.auth import HTTPBasicAuth

from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(ADMIN)
AUTH_HEADER_CACHE = "TODOKU_AUTH_HEADER"


class MailClient:
    """
    Custom email client to integrate with TODOKU email service.
    Access tokens are used in token-based authentication.
    """

    def __init__(self, send_email_url, client_id, client_secret, headers=None, data=None):
        self.send_email_url = send_email_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.headers = headers or {'Content-Type': 'application/x-www-form-urlencoded'}
        self.payload = data or 'Grant_type=client_credentials'
        self.auth = HTTPBasicAuth(self.client_id, self.client_secret)

    def send_raw_email(self, subject="", source=None, destinations=None, raw_message='', html_message=''):
        """
        Used to send email as text or HTML.
        Args:
            subject: str
            source: str
            destinations: str
            raw_message: text
            html_message: text/html

        Returns: object

        """
        log_extra = {
            "username": "unknown",
            "action": "TodokuSendEmail",
        }
        from_email = source or settings.DEFAULT_FROM_EMAIL
        message_body = {"text": raw_message}
        if html_message:
            message_body['html'] = html_message

        body = {
            "delivery": [
                {
                    "mailing-list": [{"to": {"address": receiver}} for receiver in destinations],
                    "contents": {
                        "subject": subject,
                        "body": message_body,
                        "encode": 0,  # UTF-8
                    },
                    "settings": {
                        "send_time": "now",
                        "from": {
                            "address": from_email
                        }
                    }
                },
            ]
        }
        try:
            auth_headers = cache.get(AUTH_HEADER_CACHE)
            if auth_headers is not None:
                response = requests.post(self.send_email_url, headers=auth_headers, json=body)
                data = response.json()
                if data.get("message") == "invalid token":
                    self.get_access_token()
                    response = requests.post(self.send_email_url, headers=self.headers, json=body)
            else:
                self.get_access_token()
                response = requests.post(self.send_email_url, headers=self.headers, json=body)
            if not response.ok:
                logger.debug(response.content, extra=log_extra)
                raise requests.exceptions.RequestException("Cannot send email")
        except requests.exceptions.HTTPError as e:
            logger.error(e, extra=log_extra)
        except requests.exceptions.ConnectionError as e:
            logger.error(e, extra=log_extra)
        except requests.exceptions.Timeout as e:
            logger.error(e, extra=log_extra)
        except requests.exceptions.RequestException as e:
            logger.error(e, extra=log_extra)
        else:
            logger.debug(f"Send mail success: {response.json()}", extra=log_extra)
            return response
        raise GenericException("TodokuServerError")

    def get_access_token(self, auth_token_url=None):
        """
        Get access token for authentication when sending email
        Args:
            auth_token_url: str

        Returns: str

        """
        log_extra = {
            "username": "unknown",
            "action": "TodokuAuthToken",
        }

        response = requests.post(
            auth_token_url or settings.TODOKU_AUTH_TOKEN_URL,
            headers=self.headers,
            auth=self.auth,
            data=self.payload
        )

        if not response.ok:
            logger.debug(response.content, extra=log_extra)
            raise requests.exceptions.RequestException("Cannot get access token")

        self.access_token = response.json().get("access_token")
        self.headers.update({"Authorization": f"Bearer {self.access_token}"})
        cache.set(AUTH_HEADER_CACHE, self.headers, settings.TODOKU_ACCESS_TOKEN_REFRESH_TIME)
        return self.access_token

    def status(self, delivery_id):
        """
        Use delivery_id to check status of sent email
        Args:
            delivery_id: str

        Returns: dict

        """
        response = requests.get(f"{self.send_email_url}/{delivery_id}", headers=self.headers)
        return response.json()
