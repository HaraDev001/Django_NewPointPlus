from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse
from drf_spectacular.types import OpenApiTypes

from rest_framework import views

from v1_card.serializers.access_token_serializer import (
    AccessTokenIssueRequestSerializer,
    AccessTokenIssueResponseSerializer,
    AccessTokenUpdateRequestSerializer,
    AccessTokenDeleteRequestSerializer
)
from v1_card.serializers.common_serializers import (
    CommonSerializer,
    OpenApiAccessTokenIssueSerializer,
    OpenApiAccessTokenUpdateSerializer
)


@extend_schema(
    tags=['認証関連']
)
class AuthAPIView(views.APIView):

    @extend_schema(
        summary='カードアクセストークン発行API',
        description='カード番号とPINで認証を行い、API実行に利用するトークンを発行する。',
        parameters=[
            OpenApiParameter("card_number", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("pin_number", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
        ],
        responses={
            200: OpenApiAccessTokenIssueSerializer,
            400: OpenApiResponse(
                response=CommonSerializer,
                description='PIN不一致\t\n存在しないカード'),
            403: OpenApiResponse(
                response=CommonSerializer,
                description='サービス利用許可なし\t\n事業者における利用規約未同意\t\n決済可能な状態ではないカード')
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
        summary='カードアクセストークン更新API',
        description='カードアクセストークンを更新する。',
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
                description='サービス利用許可なし\t\n事業者における利用規約未同意')
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
        summary='カードアクセストークン失効API',
        description='カードアクセストークンを失効する。',
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
