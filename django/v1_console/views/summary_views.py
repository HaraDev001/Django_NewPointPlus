from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from v1_console.permissions import (GetBalanceSummaryPermission, GetCardSummaryPermission, GetEventSummaryPermission,
                                    GetIssueTotalSummaryPermission, GetIssueTransitionSummaryPermission)
from v1_console.serializers.common_serializers import (CommonSerializer, OpenApiBalanceSummarySerializer,
                                                       OpenApiCardIssueTotalSummarySerializer,
                                                       OpenApiCardIssueTransitionSummarySerializer,
                                                       OpenApiCardTransactionSummarySerializer,
                                                       OpenApiEventSummarySerializer)
from v1_console.views.base import ConsoleBaseView


class CardTransactionSummaryAPIView(ConsoleBaseView):
    permission_classes = (GetCardSummaryPermission,)

    @extend_schema(
        summary="カード取引集計取得API",
        description="カードにおける取引の集計結果を取得する",
        parameters=[
            OpenApiParameter("auth_token", OpenApiTypes.STR,
                             OpenApiParameter.HEADER),
            OpenApiParameter("provider_id", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("aggregation_criteria", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("start_aggregation_at", OpenApiTypes.DATE,
                             OpenApiParameter.QUERY),
            OpenApiParameter("end_aggregation_at", OpenApiTypes.DATE,
                             OpenApiParameter.QUERY),
            OpenApiParameter("card_config_id", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("corporate_number", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("shop_number", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("terminal_number", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("management_tag", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
        ],
        responses={
            200: OpenApiCardTransactionSummarySerializer,
            400: OpenApiResponse(
                response=CommonSerializer,
                description='集計日時の終了日時が開始日時よりも前の日時\t\n存在しないカード設定\t\n存在しない企業\t\n存在しない店舗\t\n存在しない店舗端末\t\n存在しない管理タグ'),
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


class EventSummaryAPIView(ConsoleBaseView):
    permission_classes = (GetEventSummaryPermission,)

    @extend_schema(
        summary="イベント別集計取得",
        description="イベント別での取引の集計結果を取得する",
        parameters=[
            OpenApiParameter("auth_token", OpenApiTypes.STR,
                             OpenApiParameter.HEADER),
            OpenApiParameter("provider_id", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("aggregation_criteria", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("start_aggregation_at", OpenApiTypes.DATE,
                             OpenApiParameter.QUERY),
            OpenApiParameter("end_aggregation_at", OpenApiTypes.DATE,
                             OpenApiParameter.QUERY),
            OpenApiParameter("card_config", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("corporate_number", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("shop_number", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("terminal_number", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("management_tag", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("campaign_id", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
        ],
        responses={
            200: OpenApiEventSummarySerializer,
            400: OpenApiResponse(
                response=CommonSerializer,
                description='集計日時の終了日時が開始日時よりも前の日時\t\n存在しないカード設定\t\n存在しない企業\t\n存在しない店舗\t\n存在しない店舗端末\t\n存在しない管理タグ\t\n存在しない強制付与\t\n存在しないキャンペーン'),  # noqa: E501
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


class BalanceSummaryAPIView(ConsoleBaseView):
    permission_classes = (GetBalanceSummaryPermission,)

    @extend_schema(
        summary="基準日未使用残高集計取得API",
        description="発行保証金供託に必要な前払い式支払手段の基準日における集計結果を取得する",
        parameters=[
            OpenApiParameter("auth_token", OpenApiTypes.STR,
                             OpenApiParameter.HEADER),
            OpenApiParameter("provider_id", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("aggregation_criteria", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("start_aggregation_at", OpenApiTypes.DATE,
                             OpenApiParameter.QUERY),
            OpenApiParameter("end_aggregation_at", OpenApiTypes.DATE,
                             OpenApiParameter.QUERY),
            OpenApiParameter("card_config_id", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
        ],
        responses={
            200: OpenApiBalanceSummarySerializer,
            400: OpenApiResponse(
                response=CommonSerializer,
                description='集計日時の終了日時が開始日時よりも前の日時\t\n存在しないカード設定'),
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


class CardIssueTotalSummaryAPIView(ConsoleBaseView):
    permission_classes = (GetIssueTotalSummaryPermission,)

    @extend_schema(
        summary="カード発行数集計取得API",
        description="カードの発行数の集計を取得する",
        parameters=[
            OpenApiParameter("auth_token", OpenApiTypes.STR,
                             OpenApiParameter.HEADER),
            OpenApiParameter("provider_id", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("aggregation_criteria", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("start_aggregation_at", OpenApiTypes.DATE,
                             OpenApiParameter.QUERY),
            OpenApiParameter("end_aggregation_at", OpenApiTypes.DATE,
                             OpenApiParameter.QUERY),
            OpenApiParameter("card_config_id", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
        ],
        responses={
            200: OpenApiCardIssueTotalSummarySerializer,
            400: OpenApiResponse(
                response=CommonSerializer,
                description='集計日時の終了日時が開始日時よりも前の日時\t\n存在しないカード設定'),
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


class CardIssueTransitionSummaryAPIView(ConsoleBaseView):
    permission_classes = (GetIssueTransitionSummaryPermission,)

    @extend_schema(
        summary="カード推移集計取得API",
        description="カードの状態推移の集計を取得する",
        parameters=[
            OpenApiParameter("auth_token", OpenApiTypes.STR,
                             OpenApiParameter.HEADER),
            OpenApiParameter("provider_id", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("aggregation_criteria", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("start_aggregation_at", OpenApiTypes.DATE,
                             OpenApiParameter.QUERY),
            OpenApiParameter("end_aggregation_at", OpenApiTypes.DATE,
                             OpenApiParameter.QUERY),
        ],
        responses={
            200: OpenApiCardIssueTransitionSummarySerializer,
            400: OpenApiResponse(
                response=CommonSerializer,
                description='集計日時の終了日時が開始日時よりも前の日時\t\n存在しないカード設定'),
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
