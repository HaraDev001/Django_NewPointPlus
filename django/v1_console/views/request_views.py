from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse
from drf_spectacular.types import OpenApiTypes

from rest_framework import views

from v1_console.serializers.common_serializers import (
    CommonSerializer,
    OpenApiRequestListSerializer,
    OpenApiTransactionCancelRequestDetailSerializer
)


class RequestListAPIView(views.APIView):
    @extend_schema(
        summary="申請一覧取得",
        description="各種操作（諸変更や取引取消等）の申請の一覧を取得する",
        parameters=[
            OpenApiParameter("auth_token", OpenApiTypes.STR,
                             OpenApiParameter.HEADER),
            OpenApiParameter("provider_id", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("request_start_date", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("request_end_date", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("request_user_mail_address", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("request_user_type", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("request_status", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("order", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("start_position", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),
            OpenApiParameter("get_count", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),
        ],
        responses={
            200: OpenApiRequestListSerializer,
            400: OpenApiResponse(
                response=CommonSerializer,
                description='申請日時の終了日時が開始日時よりも前の日時'),
            401: OpenApiResponse(
                response=CommonSerializer,
                description='トークン認証エラー\t\nトークン有効期限切れ'),
            403: OpenApiResponse(
                response=CommonSerializer,
                description='利用許可がないアカウント権限'),
        },
    )
    def get(self, request):
        return


class TransactionCancelRequestDetailAPIView(views.APIView):
    @extend_schema(
        summary="取引取消申請詳細取得",
        description="取引取消申請の詳細情報を取得する",
        parameters=[
            OpenApiParameter("auth_token", OpenApiTypes.STR,
                             OpenApiParameter.HEADER),
            OpenApiParameter("provider_id", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("request_id", OpenApiTypes.STR,
                             OpenApiParameter.QUERY)
        ],
        responses={
            200: OpenApiTransactionCancelRequestDetailSerializer,
            401: OpenApiResponse(
                response=CommonSerializer,
                description='トークン認証エラー\t\nトークン有効期限切れ'),
            403: OpenApiResponse(
                response=CommonSerializer,
                description='サービス利用許可なし、利用許可がないアカウント権限'),
            404: OpenApiResponse(
                response=CommonSerializer,
                description='存在しない取引')
        }
    )
    def get(self, request, pk=None):
        return
