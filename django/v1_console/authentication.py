import logging

from config.exceptions import GenericException
from config.logging import ADMIN
from database.models import ConsoleAccount
from rest_framework_simplejwt.authentication import JWTAuthentication
from v1_console.utils import COGNITO_EXCEPTION, verify_token

logger = logging.getLogger(ADMIN)


class CognitoAuthentication(JWTAuthentication):
    """
    An authentication class requests using AWS Cognito
    """

    def get_validated_token(self, raw_token):
        """
        Return raw token no using validation of simple jwt
        """
        return raw_token

    def get_user(self, validated_token):
        """
        Attempts to find and return a user using the given validated token.
        """
        log_extra = {
            "username": "unknown",
            "action": "VerifyToken"
        }
        try:
            token_verified = verify_token(validated_token.decode())
            user_attr = token_verified['UserAttributes']
            # Get email value from UserAttributes
            email_attr = filter(lambda attr: attr['Name'] == 'email', user_attr)
            email = list(email_attr)[0]['Value']

            # Assuming that 1 email - 1 provider
            return ConsoleAccount.objects.get(email=email)   # TODO: rewrite when implementing multiple provider_id

        except COGNITO_EXCEPTION.NotAuthorizedException:
            logger.error("Invalid Token", extra=log_extra)
            raise GenericException("TokenAuthenticationError")
        except ConsoleAccount.DoesNotExist:
            logger.error("ConsoleAccount: User does not exist ", extra=log_extra)
            raise GenericException("TokenAuthenticationError")
