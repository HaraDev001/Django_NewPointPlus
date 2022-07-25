from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from v1_console.permissions import ExportCardCsvPermission, GetCardDetailPermission, GetCardListPermission
from v1_console.serializers.common_serializers import (CommonSerializer, OpenApiCardDetailSerializer,
                                                       OpenApiCardListCsvSerializer, OpenApiCardListSerializer)
from v1_console.views.base import ConsoleBaseView


class CardListAPIView(ConsoleBaseView):
    permission_classes = (GetCardListPermission, )

    @extend_schema(
        summary="カード一覧取得",
        description="カードの一覧を取得する",
        parameters=[
            OpenApiParameter("auth_token", OpenApiTypes.STR,
                             OpenApiParameter.HEADER),
            OpenApiParameter("start_position", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),
            OpenApiParameter("get_count", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),
            OpenApiParameter("card_config_name", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("card_config_type", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),
            OpenApiParameter("card_status", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),
            OpenApiParameter("card_number", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),
            OpenApiParameter("test_card_flag", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),
        ],
        responses={
            200: OpenApiCardListSerializer,
            400: OpenApiResponse(
                response=CommonSerializer,
                description='存在しないカード設定'),
            401: OpenApiResponse(
                response=CommonSerializer,
                description='トークン認証エラー\t\nトークン有効期限切れ'),
            403: OpenApiResponse(
                response=CommonSerializer,
                description='サービス利用許可なし\t\n利用許可がないアカウント権限')
        }
    )
    def get(self, request):
        return


class CardDetailAPIView(ConsoleBaseView):
    permission_classes = (GetCardDetailPermission, )

    @extend_schema(
        summary="カード詳細取得",
        description="カードの詳細情報を取得する",
        parameters=[
            OpenApiParameter("auth_token", OpenApiTypes.STR,
                             OpenApiParameter.HEADER),
            OpenApiParameter("card_number", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),
        ],
        responses={
            200: OpenApiCardDetailSerializer,
            401: OpenApiResponse(
                response=CommonSerializer,
                description='トークン認証エラー\t\nトークン有効期限切れ'),
            403: OpenApiResponse(
                response=CommonSerializer,
                description='サービス利用許可なし\t\n利用許可がないアカウント権限'),
            404: OpenApiResponse(
                response=CommonSerializer,
                description='存在しないカード'),
        }
    )
    def get(self, request, pk=None):
        return


class CardListCsvAPIView(ConsoleBaseView):
    permission_classes = (ExportCardCsvPermission, )

    @extend_schema(
        summary="カード一覧CSV取得",
        description="カード一覧情報をCSV形式で取得する",
        # 認証トークン
        # 取得開始位置、取得件数
        # 検索（カード設定ID / カード設定種別 / カード状態 / テストカードフラグ / 取引期間）
        parameters=[
            OpenApiParameter("auth_token", OpenApiTypes.STR,
                             OpenApiParameter.HEADER),
            OpenApiParameter("provider_id", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("start_position", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),
            OpenApiParameter("get_count", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),
            OpenApiParameter("card_config_name", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("card_config_type", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),
            OpenApiParameter("card_status", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),
            OpenApiParameter("card_number", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),
            OpenApiParameter("test_card_flag", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),
        ],
        responses={
            200: OpenApiCardListCsvSerializer,
            400: OpenApiResponse(
                response=CommonSerializer,
                description='存在しないカード設定'),
            401: OpenApiResponse(
                response=CommonSerializer,
                description='トークン認証エラー\t\nトークン有効期限切れ'),
            403: OpenApiResponse(
                response=CommonSerializer,
                description='サービス利用許可なし\t\n利用許可がないアカウント権限')
        }
    )
    def post(self, request, pk=None):
        return
