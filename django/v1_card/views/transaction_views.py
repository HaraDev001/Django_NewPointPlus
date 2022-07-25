from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework import views
from ..serializers.transaction_serializers import TransactionRequestSerializer, \
    TransactionListRequestSerializer
import json
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse
from drf_spectacular.types import OpenApiTypes

from v1_card.serializers.common_serializers import (
    CommonSerializer,
    OpenApiTransactionListSerializer,
    OpenApiTransactionDetailSerializer
)


@extend_schema(
    tags=['取引関連']
)
class TransactionListAPIView(views.APIView):
    @extend_schema(
        summary='取引履歴一覧取得API',
        description='取引履歴の一覧を取得する。',
        operation_id='cards_transactions_list',
        # 取得開始位置、取得件数
        # 検索（取引種別 / 取引日時（開始日時 / 終了日時）/ 取引状態）
        # 降順/昇順指定(取引日時)
        parameters=[
            OpenApiParameter("auth_token", OpenApiTypes.STR,
                             OpenApiParameter.HEADER),
            OpenApiParameter("start_position", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),
            OpenApiParameter("get_count", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),
            OpenApiParameter("transaction_type", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),
            OpenApiParameter("transaction_at", OpenApiTypes.DATE,
                             OpenApiParameter.QUERY),
            OpenApiParameter("transaction_status", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),
            OpenApiParameter("transaction_at_order", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),
        ],
        responses={
            200: OpenApiTransactionListSerializer,
            400: OpenApiResponse(
                response=CommonSerializer,
                description='取引日時の終了日時が開始日時よりも前の日時'),
            401: OpenApiResponse(
                response=CommonSerializer,
                description='トークン認証エラー\t\nトークン有効期限切れ'),
            403: OpenApiResponse(
                response=CommonSerializer,
                description='サービス利用許可なし')
        }
    )
    def get(self, request, card_number):

        # アクセストークン情報をrequestから取得
        request_body = json.loads(request.body)
        request_body['card_no'] = card_number
        serializer = TransactionListRequestSerializer(data=request_body)
        if serializer.is_valid():
            response_data, response_status = serializer.save()
            return Response(response_data, response_status)


@extend_schema(
    tags=['取引関連']
)
class TransactionAPIView(views.APIView):
    @extend_schema(
        summary='取引履歴詳細取得API',
        description='取引履歴の詳細情報を取得する。',
        parameters=[
            OpenApiParameter("auth_token", OpenApiTypes.STR,
                             OpenApiParameter.HEADER),
            # 取引番号
            OpenApiParameter("transaction_number", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),
        ],
        responses={
            200: OpenApiTransactionDetailSerializer,
            401: OpenApiResponse(
                response=CommonSerializer,
                description='トークン認証エラー\t\nトークン有効期限切れ'),
            403: OpenApiResponse(
                response=CommonSerializer,
                description='サービス利用許可なし'),
            404: OpenApiResponse(
                response=CommonSerializer,
                description='存在しない取引'),
        }
    )
    def get(self, request, card_number, transaction_id):

        # アクセストークン情報をrequestから取得
        request_body = json.loads(request.body)
        # serializerでbusiness_logicを呼び出すために、card_numberをデータとして格納
        request_body['card_no'] = card_number
        request_body['transaction_id'] = transaction_id
        token_serializer = TransactionRequestSerializer(data=request_body)
        if token_serializer.is_valid():
            response_data, response_status = token_serializer.save()
            return Response(response_data, response_status)
