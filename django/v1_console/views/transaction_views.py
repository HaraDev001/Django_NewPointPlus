from database.models import TransactionCategory
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework.response import Response
from v1_console.permissions import (ApproveCancelTransactionRequestPermission, CancelTransactionPermission,
                                    ExportTransactionCsvPermission, GetTransactionDetailPermission,
                                    RequestCancelTransactionPermission, TransactionPermission,
                                    WithdrawalTransactionCancelRequestPermission)
from v1_console.serializers import TransactionTypeSerializer
from v1_console.serializers.common_serializers import (CommonSerializer, OpenApiIssueTransactionNumberSerializer,
                                                       OpenApiTransactionCancelRequestSerializer,
                                                       OpenApiTransactionCancelSerializer,
                                                       OpenApiTransactionDetailSerializer,
                                                       OpenApiTransactionListCsvSerializer,
                                                       OpenApiTransactionListSerializer,
                                                       OpenApiTransactionTypeListSerializer)
from v1_console.views import ConsoleBaseView


class TransactionListAPIView(ConsoleBaseView):
    permission_classes = (TransactionPermission, )

    @extend_schema(
        summary="取引履歴一覧取得",
        description="取引履歴の一覧を取得する",
        parameters=[
            OpenApiParameter("auth_token", OpenApiTypes.STR,
                             OpenApiParameter.HEADER),
            OpenApiParameter("provider_id", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("start_position", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),
            OpenApiParameter("get_count", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),
            OpenApiParameter("transaction_type", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),
            OpenApiParameter("start_transaction_at", OpenApiTypes.DATE,
                             OpenApiParameter.QUERY),
            OpenApiParameter("end_transaction_at", OpenApiTypes.DATE,
                             OpenApiParameter.QUERY),
            OpenApiParameter("transaction_status", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),
            OpenApiParameter("corporate_number", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("shop_number", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("terminal_number", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),
            OpenApiParameter("card_config_name", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("card_number", OpenApiTypes.INT, OpenApiParameter.QUERY),
            OpenApiParameter("test_card_flag", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),
            OpenApiParameter("transaction_date_order", OpenApiTypes.INT,
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
                description='サービス利用許可なし\t\n利用許可がないアカウント権限'),
            404: OpenApiResponse(
                response=CommonSerializer,
                description='存在しない取引')
        }
    )
    def get(self, request):
        return

    @extend_schema(
        summary="取引番号発行API",
        description="事前に取引で利用する取引番号の発行を行う",
        parameters=[
            OpenApiParameter("auth_token", OpenApiTypes.STR,
                             OpenApiParameter.HEADER),
        ],
        responses={
            200: OpenApiIssueTransactionNumberSerializer,
            401: OpenApiResponse(
                response=CommonSerializer,
                description='トークン認証エラー\t\nトークン有効期限切れ'),
        }
    )
    def post(self, request):
        return


class TransactionDetailAPIView(ConsoleBaseView):
    permission_classes = (GetTransactionDetailPermission,)

    @extend_schema(
        summary="取引履歴詳細取得",
        description="取引履歴の詳細情報を取得する",
        parameters=[
            OpenApiParameter("auth_token", OpenApiTypes.STR,
                             OpenApiParameter.HEADER),
            OpenApiParameter("provider_id", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("transaction_number", OpenApiTypes.INT, OpenApiParameter.QUERY),
        ],
        responses={
            200: OpenApiTransactionDetailSerializer,
            401: OpenApiResponse(
                response=CommonSerializer,
                description='トークン認証エラー\t\nトークン有効期限切れ'),
            403: OpenApiResponse(
                response=CommonSerializer,
                description='サービス利用許可なし\t\n利用許可がないアカウント権限'),
            404: OpenApiResponse(
                response=CommonSerializer,
                description='存在しない取引'),
        }
    )
    def get(self, request, pk=None):
        return


class TransactionListCsvAPIView(ConsoleBaseView):
    permission_classes = (ExportTransactionCsvPermission, )

    @extend_schema(
        summary="取引履歴一覧CSV取得",
        description="取引履歴一覧情報をCSV形式で取得する",
        parameters=[
            # 認証トークン
            # 取得開始位置、取得件数
            # 検索（取引種別 / 取引日時（開始日時 / 終了日時）/ 取引状態 / 企業番号 / 店舗番号 / 端末番号 / カード設定ID / カード番号 / テストカードフラグ）
            # 降順/昇順指定(取引日時)
            OpenApiParameter("auth_token", OpenApiTypes.STR,
                             OpenApiParameter.HEADER),
            OpenApiParameter("provider_id", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("start_position", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),
            OpenApiParameter("get_count", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),
            OpenApiParameter("transaction_type", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),
            OpenApiParameter("start_transaction_at", OpenApiTypes.DATE,
                             OpenApiParameter.QUERY),
            OpenApiParameter("end_transaction_at", OpenApiTypes.DATE,
                             OpenApiParameter.QUERY),
            OpenApiParameter("transaction_status", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),
            OpenApiParameter("corporate_number", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("shop_number", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("terminal_number", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),
            OpenApiParameter("card_config_id", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("card_number", OpenApiTypes.INT, OpenApiParameter.QUERY),
            OpenApiParameter("test_card_flag", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),
            OpenApiParameter("transaction_date_order", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),
        ],
        responses={
            200: OpenApiTransactionListCsvSerializer,
            400: OpenApiResponse(
                response=CommonSerializer,
                description='取引日時の終了日時が開始日時よりも前の日時\t\n存在しないカード設定'),
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


class TransactionTypeListAPIView(ConsoleBaseView):
    @extend_schema(
        summary="取引種別一覧取得",
        description="チャージや決済等の取引パターンの一覧を取得する",
        parameters=[
        ],
        responses={200: OpenApiTransactionTypeListSerializer},
    )
    def get(self, request):
        queryset = TransactionCategory.objects.all()
        serializer = TransactionTypeSerializer(queryset, many=True)
        return Response(serializer.data)


class TransactionCancelAPIView(ConsoleBaseView):
    permission_classes = (CancelTransactionPermission,)

    @extend_schema(
        summary="取引取消",
        description="過去に行った取引を取り消す",
        parameters=[
            OpenApiParameter("auth_token", OpenApiTypes.STR,
                             OpenApiParameter.HEADER),
            OpenApiParameter("provider_id", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            # 取引番号
            OpenApiParameter("transaction_number", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),
            # 取消対象取引番号
            OpenApiParameter("cancel_transaction_number", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),
            # カード番号
            OpenApiParameter("card_number", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),
            # 集計対象先(企業)
            OpenApiParameter("aggregation_company", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            # 集計対象先(店舗)
            OpenApiParameter("aggregation_shop", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            # 集計対象先(端末)
            OpenApiParameter("aggregation_terminal", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            # 操作者アカウントID
            OpenApiParameter("operator_account_id", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),

        ],
        # 未対応 取引完了している取引番号
        responses={
            200: OpenApiResponse(
                response=OpenApiTransactionCancelSerializer,
                description='取消済みの取引'),
            400: OpenApiResponse(
                response=CommonSerializer,
                description='異なるアカウントからのリクエスト\t\n存在しない取消対象取引\t\n存在しないカード\t\n残高不足\t\n残高上限超え'),
            401: OpenApiResponse(
                response=CommonSerializer,
                description='トークン認証エラー\t\nトークン有効期限切れ'),
            403: OpenApiResponse(
                response=CommonSerializer,
                description='サービス利用許可なし\t\n利用許可がないアカウント権限\t\nアクティベートでないカード\t\nロック状態のカード'),
            404: OpenApiResponse(
                response=CommonSerializer,
                description='存在しない取引')
        }
    )
    def put(self, request, pk=None):
        return


class TransactionCancelRequestAPIView(ConsoleBaseView):
    permission_classes = (RequestCancelTransactionPermission,)

    @ extend_schema(
        summary="取引取消申請",
        description="過去に行った取引の取り消しを申請する",
        parameters=[
            OpenApiParameter("auth_token", OpenApiTypes.STR,
                             OpenApiParameter.HEADER),
            OpenApiParameter("provider_id", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("transaction_number", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),
            # 取消対象取引番号
            OpenApiParameter("cancel_transaction_number", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),
            # カード番号
            OpenApiParameter("card_number", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),
            # メール送信フラグ
            OpenApiParameter("send_email_flag", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),

        ],
        # 未対応 取引完了している取引番号
        responses={
            200: OpenApiResponse(
                response=OpenApiTransactionCancelRequestSerializer,
                description='取消済みの取引\t\n取消申請中の取引'),
            400: OpenApiResponse(
                response=CommonSerializer,
                description='異なるアカウントからのリクエスト\t\n存在しない取消対象取引\t\n存在しないカード\t\n残高不足\t\n残高上限超え'),
            401: OpenApiResponse(
                response=CommonSerializer,
                description='トークン認証エラー\t\nトークン有効期限切れ'),
            403: OpenApiResponse(
                response=CommonSerializer,
                description='サービス利用許可なし\t\n利用許可がないアカウント権限\t\nアクティベートでないカード\t\nロック状態のカード'),
            404: OpenApiResponse(
                response=CommonSerializer,
                description='存在しない取引')
        }
    )
    def post(self, request, pk=None):
        return


class TransactionCancelRequestApproveAPIView(ConsoleBaseView):
    permission_classes = (ApproveCancelTransactionRequestPermission,)

    @extend_schema(
        summary="取引取消承認",
        description="取引取消の申請を承認または否認する",
        parameters=[
            OpenApiParameter("auth_token", OpenApiTypes.STR,
                             OpenApiParameter.HEADER),
            OpenApiParameter("provider_id", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            # 申請ID
            OpenApiParameter("request_id", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),
            # 承認フラグ
            OpenApiParameter("approval_flag", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),
            # 否認対象箇所
            OpenApiParameter("denial_point", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            # 否認理由
            OpenApiParameter("denial_reason", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            # メール送信フラグ
            OpenApiParameter("send_email_flag", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),
        ],
        # 未対応 承認待ちでない申請情報
        responses={
            200: None,
            400: OpenApiResponse(
                response=CommonSerializer,
                description='申請情報なし\t\n残高不足\t\n残高上限超え'),
            401: OpenApiResponse(
                response=CommonSerializer,
                description='トークン認証エラー\t\nトークン有効期限切れ'),
            403: OpenApiResponse(
                response=CommonSerializer,
                description='サービス利用許可なし\t\n利用許可がないアカウント権限\t\nアクティベートでないカード\t\nロック状態のカード'),
            404: OpenApiResponse(
                response=CommonSerializer,
                description='存在しない取引'),
        }
    )
    def put(self, request, pk=None, request_id=None):
        return


class TransactionCancelRequestWithdrawalAPIView(ConsoleBaseView):
    permission_classes = (WithdrawalTransactionCancelRequestPermission,)

    @extend_schema(
        summary="取引取消申請取下",
        description="取引取消の申請を取り下げる",
        parameters=[
            OpenApiParameter("auth_token", OpenApiTypes.STR,
                             OpenApiParameter.HEADER),
            OpenApiParameter("provider_id", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            # 申請ID
            OpenApiParameter("request_id", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),
            # メール送信フラグ
            OpenApiParameter("send_email_flag", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),

        ],
        # 未対応 承認待ちでない申請情報
        responses={
            200: None,
            400: OpenApiResponse(
                response=CommonSerializer,
                description='申請情報なし'),
            401: OpenApiResponse(
                response=CommonSerializer,
                description='トークン認証エラー\t\nトークン有効期限切れ'),
            403: OpenApiResponse(
                response=CommonSerializer,
                description='サービス利用許可なし\t\n利用許可がないアカウント権限'),
            404: OpenApiResponse(
                response=CommonSerializer,
                description='存在しない取引'),
        }
    )
    def put(self, request, pk=None, request_id=None):
        return
