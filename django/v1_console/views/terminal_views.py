from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse
from drf_spectacular.types import OpenApiTypes

from rest_framework import views

from v1_console.serializers.common_serializers import (
    CommonSerializer,
    OpenApiTerminalListSerializer
)


class TerminalListAPIView(views.APIView):
    @extend_schema(
        summary="店舗端末一覧取得",
        description="店舗に紐付く端末の一覧を取得する",
        parameters=[
            OpenApiParameter("auth_token", OpenApiTypes.STR,
                             OpenApiParameter.HEADER),
            OpenApiParameter("provider_id", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("terminal_type", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("terminal_number", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("management_tag", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            # ステータス
            OpenApiParameter("status", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
        ],
        responses={
            200: OpenApiTerminalListSerializer,
            401: OpenApiResponse(
                response=CommonSerializer,
                description='トークン認証エラー\t\nトークン有効期限切れ'),
            403: OpenApiResponse(
                response=CommonSerializer,
                description='利用許可がないアカウント権限')
        }
    )
    def get(self, request):
        return
