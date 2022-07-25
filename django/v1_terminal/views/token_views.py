from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse
from drf_spectacular.types import OpenApiTypes

from rest_framework import views
from rest_framework.response import Response

from v1_terminal.serializers.access_token_serializer import (
    AccessTokenIssueRequestSerializer,
    AccessTokenIssueResponseSerializer,
    AccessTokenUpdateRequestSerializer,
    AccessTokenDeleteRequestSerializer
)
from v1_terminal.serializers.common_serializers import (
    CommonSerializer,
    OpenApiAccessTokenIssueSerializer,
    OpenApiAccessTokenUpdateSerializer
)


@extend_schema(
    tags=['トークン関連']
)
class TokenAPIView(views.APIView):

    @extend_schema(
        summary="店舗端末アクセストークン発行",
        description="端末番号で認証を行い、API実行に利用するトークンを発行する",
        parameters=[
            # メールアドレス
            OpenApiParameter("email", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            # ログインパスワード
            OpenApiParameter("login_password", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            # 端末番号
            OpenApiParameter("terminal_number", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
        ],
        responses={
            200: OpenApiAccessTokenIssueSerializer,
            400: OpenApiResponse(
                response=CommonSerializer,
                description='存在しない店舗端末'),
            401: OpenApiResponse(
                response=CommonSerializer,
                description='メールアドレスまたはログインパスワードが違う'),
            403: OpenApiResponse(
                response=CommonSerializer,
                description='有効でないアカウント\t\n事業者における利用規約未同意\t\n有効でない店舗端末')
        }
    )
    def post(self, request):
        serializer = AccessTokenIssueRequestSerializer(data=request.data)
        if serializer.is_valid():
            access_token_issue_response, status_code = serializer.save()
            if access_token_issue_response is not None:
                response_serializer = AccessTokenIssueResponseSerializer(
                    access_token_issue_response)
                return Response(response_serializer.data, status_code,
                                content_type='application/json')
            else:
                return Response(status=status_code)

    @extend_schema(
        summary="店舗端末アクセストークン更新",
        description="店舗端末アクセストークンを更新する",
        parameters=[
            OpenApiParameter("refresh_token", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
        ],
        responses={
            200: OpenApiAccessTokenUpdateSerializer,
            400: OpenApiResponse(
                response=CommonSerializer,
                description='存在しないリフレッシュトークン'),
            403: OpenApiResponse(
                response=CommonSerializer,
                description='事業者における利用規約未同意')
        }
    )
    def put(self, request):
        serializer = AccessTokenUpdateRequestSerializer(data=request.data)
        if serializer.is_valid():
            access_token_issue_response, status_code = serializer.save()
            if access_token_issue_response is not None:
                response_serializer = AccessTokenIssueResponseSerializer(
                    access_token_issue_response)
                return Response(response_serializer.data, status_code,
                                content_type='application/json')
            else:
                return Response(status=status_code)

    @extend_schema(
        summary="店舗端末アクセストークン失効",
        description="店舗端末アクセストークンを失効する",
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
                description='存在しない認証トークン\t\n存在しないリフレッシュトークン')
        }
    )
    def delete(self, request):
        serializer = AccessTokenDeleteRequestSerializer(data=request.data)
        if serializer.is_valid():
            status_code = serializer.save()
            return Response(status=status_code)
