import json
import logging
from datetime import timedelta

from config.exceptions import GenericException
from config.logging import ADMIN
from database.models import ConsoleAccount
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.response import Response
from v1_console.permissions import TokenPermission
from v1_console.serializers import (AuthIssueTokenSerializer, AuthRevokeTokenSerializer, AuthUpdateTokenSerializer,
                                    CommonSerializer)
from v1_console.serializers.common_serializers import (OpenApiAccessTokenIssueSerializer,
                                                       OpenApiAccessTokenUpdateSerializer)
from v1_console.utils import COGNITO_EXCEPTION, get_init_pass_url, issue_token, revoke_token, update_token
from v1_console.views.base import ConsoleBaseView

from django.core.mail import send_mail
from django.utils import timezone

logger = logging.getLogger(ADMIN)


class AuthAPIView(ConsoleBaseView):
    permission_classes = (TokenPermission, )

    @extend_schema(
        summary="事業者アクセストークン発行",
        description="管理Webのアカウントで認証を行い、API実行に利用するトークンを発行する",
        parameters=[
            # メールアドレス
            OpenApiParameter("email", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            # ログインパスワード
            OpenApiParameter("login_password", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            # メール送信フラグ
            OpenApiParameter("send_email_flag", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),
        ],
        responses={
            200: OpenApiResponse(
                response=OpenApiAccessTokenIssueSerializer,
                description='初回ログイン'),
            401: OpenApiResponse(
                response=CommonSerializer,
                description='メールアドレスまたはログインパスワードが違う'),
            403: OpenApiResponse(
                response=CommonSerializer,
                description='有効でないアカウント\t\n事業者における利用規約未同意(オーナー以外)')
        }
    )
    def post(self, request):
        log_extra = {
            "username": request.data.get('email'),
            "action": "Login",
        }
        logger.info("Start api Login", extra=log_extra)
        serializer = AuthIssueTokenSerializer(data=request.data)
        if not serializer.is_valid():
            logger.error(serializer.errors, extra=log_extra)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        valid_data = serializer.validated_data
        # check if user exist in ConsoleAccount or not
        try:
            ConsoleAccount.objects.get(email=valid_data['email'])
        except ConsoleAccount.DoesNotExist:
            logger.error("ConsoleAccount: User does not exist", extra=log_extra)
            raise GenericException("LoginError")

        if valid_data['send_email_flag']:
            logger.info("Sending email to user", extra=log_extra)
            # TODO: confirm send mail
            pass

        try:
            cognito_response = issue_token(valid_data['email'], valid_data['login_password'])
            now = timezone.now()
            auth_result = cognito_response.get('AuthenticationResult')
            if not auth_result and cognito_response.get('ChallengeName') == 'NEW_PASSWORD_REQUIRED':
                logger.info("First Login", extra=log_extra)
                session = cognito_response['Session']
                user_atr = cognito_response['ChallengeParameters']['userAttributes']
                email = json.loads(user_atr).get('email')
                url = get_init_pass_url(email, session)
                send_mail(
                    subject="[ARARA] NEW PASSWORD REQUIRED",  # TODO: confirm email template
                    message=url,
                    html_message=url,
                    from_email=None,  # Use the value of the DEFAULT_FROM_EMAIL setting
                    recipient_list=[email],
                )
                raise GenericException("FirstLogin")

            token = auth_result.get('AccessToken')
            if not token:
                logger.error("Cognito doesn't return token", extra=log_extra)
                raise GenericException("TokenAuthenticationError")

            # TODO Collect agreement status of terms
            agree = True
            if not agree:  # TODO: confirm business flow
                logger.error("User does not agree terms of service", extra=log_extra)
                raise GenericException("DisagreeTermsOfUse")

            response_data = {
                'token': token,
                'token_expiration_date': now + timedelta(seconds=int(auth_result['ExpiresIn'])),
                'refresh_token': auth_result['RefreshToken'],
                'terms_of_service_disagreement_flag': agree,
            }
            return Response(data=response_data, status=status.HTTP_200_OK)

        except COGNITO_EXCEPTION.NotAuthorizedException:
            logger.error("Incorrect credential", extra=log_extra)
            raise GenericException("LoginError")
        except COGNITO_EXCEPTION.UserNotFoundException:
            logger.error("Cognito: User does not exist", extra=log_extra)
            raise GenericException("LoginError")
        finally:
            logger.info("End api process", extra=log_extra)

    @extend_schema(
        summary="事業者アクセストークン更新",
        description="認証トークンの更新処理を行う",
        parameters=[
            OpenApiParameter("refresh_token", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("provider_id", OpenApiTypes.STR,
                             OpenApiParameter.QUERY)
        ],
        responses={
            200: OpenApiAccessTokenUpdateSerializer,
            400: OpenApiResponse(
                response=CommonSerializer,
                description='存在しないリフレッシュトークン'),
            403: OpenApiResponse(
                response=CommonSerializer,
                description='事業者における利用規約未同意(オーナー以外)')
        }
    )
    def put(self, request, pk=None):
        log_extra = {
            "username": "unknown",
            "action": "UpdateToken",
        }
        logger.info("Start api UpdateToken", extra=log_extra)
        serializer = AuthUpdateTokenSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            response = update_token(serializer.validated_data['refresh_token'])
            now = timezone.now()
            auth_result = response.get('AuthenticationResult')
            if not auth_result:
                logger.error("Cognito doesn't return data", extra=log_extra)
                raise GenericException("TokenAuthenticationError")

            token = auth_result.get('AccessToken')
            if not token:
                logger.error("Cognito doesn't return token", extra=log_extra)
                raise GenericException("TokenAuthenticationError")

            agree = True
            if not agree:  # TODO: confirm flow
                logger.error("User dose not agree terms of service", extra=log_extra)
                raise GenericException("DisagreeTermsOfUse")

            response_data = {
                'token': token,
                'token_expiration_date': now + timedelta(seconds=int(auth_result['ExpiresIn'])),
                'terms_of_service_disagreement_flag': agree,
            }
            return Response(data=response_data, status=status.HTTP_200_OK)

        except COGNITO_EXCEPTION.NotAuthorizedException:
            logger.error("Incorrect credential", extra=log_extra)
            raise GenericException("TokenAuthenticationError")

        finally:
            logger.info("End api process", extra=log_extra)

    @extend_schema(
        summary="事業者アクセストークン失効",
        description="認証トークンの失効処理を行う",
        parameters=[
            OpenApiParameter("auth_token", OpenApiTypes.STR,
                             OpenApiParameter.HEADER),
            OpenApiParameter("refresh_token", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
        ],
        responses={
            200: None,
            400: OpenApiResponse(
                response=CommonSerializer,
                description='存在しない認証トークン\t\n存在しないリフレッシュトークン'),
        }
    )
    def delete(self, request, pk=None):
        log_extra = {
            "username": request.user.email,
            "action": "RevokeToken",
        }
        logger.info("Start api RevokeToken", extra=log_extra)
        serializer = AuthRevokeTokenSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            revoke_token(serializer.validated_data['refresh_token'])
            return Response(status=status.HTTP_200_OK)

        except COGNITO_EXCEPTION.UnauthorizedException:
            logger.error("Invalid credential", extra=log_extra)
            raise GenericException("TokenAuthenticationError")

        finally:
            logger.info("End api process", extra=log_extra)
