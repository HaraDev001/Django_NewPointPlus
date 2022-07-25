import json
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse
from drf_spectacular.types import OpenApiTypes

from rest_framework import views
from rest_framework.response import Response
from v1_card.serializers import (AccessTokenCardBalanceRequestSerializer,
                                 AccessTokenCardDetailRequestSerializer)

from v1_card.serializers.common_serializers import (
    CommonSerializer,
    OpenApiCardDetailSerializer,
    OpenApiBalanceSerializer
)


@extend_schema(
    tags=['カード関連']
)
class CardAPIView(views.APIView):

    @extend_schema(
        summary='カード詳細取得API',
        description='カードの詳細情報を取得する。',
        parameters=[
            OpenApiParameter("auth_token", OpenApiTypes.STR,
                             OpenApiParameter.HEADER),
        ],
        responses={
            200: OpenApiCardDetailSerializer,
            401: OpenApiResponse(
                response=CommonSerializer,
                description='トークン認証エラー\t\nトークン有効期限切れ'),
            403: OpenApiResponse(
                response=CommonSerializer,
                description='サービス利用許可なし'),
            404: OpenApiResponse(
                response=CommonSerializer,
                description='存在しないカード')
        }
    )
    def get(self, request, card_number):
        request_body = json.loads(request.body)
        # serializerでbusiness_logicを呼び出すために、card_numberをデータとして格納
        request_body['card_no'] = card_number
        token_serializer = AccessTokenCardDetailRequestSerializer(
            data=request_body)
        if token_serializer.is_valid():
            response_data, response_status = token_serializer.save()
            return Response(response_data, response_status)


@extend_schema(
    tags=['カード関連']
)
class BalanceAPIView(views.APIView):

    @extend_schema(
        summary='残高照会API',
        description='カードの残高を取得する。',
        parameters=[
            OpenApiParameter("auth_token", OpenApiTypes.STR,
                             OpenApiParameter.HEADER),
        ],
        responses={
            200: OpenApiBalanceSerializer,
            401: OpenApiResponse(
                response=CommonSerializer,
                description='トークン認証エラー\t\nトークン有効期限切れ'),
            403: OpenApiResponse(
                response=CommonSerializer,
                description='サービス利用許可なし'),
            404: OpenApiResponse(
                response=CommonSerializer,
                description='存在しないカード')
        }
    )
    def get(self, request, card_number):

        request_body = json.loads(request.body)
        # serializerでbusiness_logicを呼び出すために、card_numberをデータとして格納
        request_body['card_no'] = card_number
        token_serializer = AccessTokenCardBalanceRequestSerializer(
            data=request_body)
        if token_serializer.is_valid():
            response_data, response_status = token_serializer.save()
            return Response(response_data, response_status)
        return
