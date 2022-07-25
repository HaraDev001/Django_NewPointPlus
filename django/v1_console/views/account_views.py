import logging

from config.exceptions import GenericException
from config.logging import ADMIN
from database.models import ConsoleAccount, PermissionManagement
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework import generics, status, views
from rest_framework.response import Response
from v1_console.serializers import OperationPermissionListSerializer
from v1_console.serializers.account_serializers import InitializePwdRequestSerializer
from v1_console.serializers.common_serializers import CommonSerializer, OpenApiOperationPermissionListSerializer
from v1_console.utils import COGNITO_EXCEPTION, set_initial_password
from v1_console.views.base import ConsoleBaseView

from django.core.exceptions import ValidationError

logger = logging.getLogger(ADMIN)


class SetPasswordAPIView(views.APIView):
    @extend_schema(
        summary="アカウント初期パスワード変更",
        description="初回ログイン時に初期パスワードを変更する",
        parameters=[
            OpenApiParameter("email", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            # ログインパスワード
            OpenApiParameter("login_password", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            # セッション
            OpenApiParameter("session", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
        ],
        responses={
            200: None,
            401: OpenApiResponse(
                response=CommonSerializer,
                description='セッションエラー\t\n初期パスワード不一致'),
        }
    )
    def put(self, request):
        log_extra = {
            "username": request.data.get('email'),
            "action": "SetInitialPwd",
        }

        logger.info("Start api Set initial password", extra=log_extra)
        serializer = InitializePwdRequestSerializer(data=request.data)

        if not serializer.is_valid():
            logger.error(serializer.errors, extra=log_extra)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            data = serializer.validated_data
            email = data.get("email")
            login_password = data.get("login_password")
            session = data.get("session")
            set_initial_password(email, login_password, session)

            return Response(status=status.HTTP_200_OK)

        except COGNITO_EXCEPTION.NotAuthorizedException:
            logger.error("Session errors", extra=log_extra)
            raise GenericException("TokenAuthenticationError")
        except COGNITO_EXCEPTION.CodeMismatchException:
            logger.error("Invalid session", extra=log_extra)
            raise GenericException("TokenAuthenticationError")
        finally:
            logger.info("End api process", extra=log_extra)


class OperationPermissionListAPIView(ConsoleBaseView, generics.ListAPIView):
    queryset = PermissionManagement.objects.order_by('permission__name')
    serializer_class = OperationPermissionListSerializer
    pagination_class = None

    def get_account(self):
        log_extra = {
            "username": self.request.user.email,
            "action": "GetPermission",
        }
        query = {'email': self.request.user.email}
        provider_id = self.request.query_params.get('provider_id')
        if provider_id:
            query['provider_id'] = provider_id

        try:
            return ConsoleAccount.objects.get(**query)
        except ConsoleAccount.DoesNotExist:
            logger.info('User not found', extra=log_extra)
            return None
        except ValidationError:
            logger.info('Invalid provider_id format', extra=log_extra)
            return None

    def get_queryset(self):
        account = self.get_account()

        if account is None:
            return self.queryset.none()

        return self.queryset \
            .filter(group=account.group) \
            .filter(role=account.role)

    @extend_schema(
        summary="アカウント操作権限一覧取得",
        description="管理アカウントの操作権限の一覧を取得する",
        parameters=[
            OpenApiParameter("auth_token", OpenApiTypes.STR,
                             OpenApiParameter.HEADER),
            OpenApiParameter("provider_id", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
        ],
        responses={
            200: OpenApiOperationPermissionListSerializer,
            401: OpenApiResponse(
                response=CommonSerializer,
                description='トークン認証エラー\t\nトークン有効期限切れ')
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(self, request, *args, **kwargs)
