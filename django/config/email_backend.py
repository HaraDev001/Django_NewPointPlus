from utils.email_utility import MailClient

from django.conf import settings


class CustomEmailBackend:
    """ The backend to use for sending emails. """

    def __init__(self, **kwargs):
        self.connection = MailClient(
            send_email_url=settings.TODOKU_SEND_EMAIL_URL,
            client_id=settings.TODOKU_CLIENT_ID,
            client_secret=settings.TODOKU_CLIENT_SECRET,
        )

    def send_messages(self, email_messages):
        for email_message in email_messages:
            html_message = email_message.alternatives[0][0] if email_message.alternatives else None
            self.connection.send_raw_email(
                subject=email_message.subject,
                source=email_message.from_email,
                destinations=email_message.recipients(),
                raw_message=email_message.body,
                html_message=html_message
            )
