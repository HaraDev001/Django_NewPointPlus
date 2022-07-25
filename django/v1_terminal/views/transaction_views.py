from drf_spectacular.utils import extend_schema
from rest_framework import views
from rest_framework.response import Response
from v1_terminal.serializers import (IssueTransactionNumberRequestSerializer,
                                    IssueTransactionNumberResponseSerializer,
                                    TransactionChargeRequestSerializers,
                                    TransactionChargeResponseSerializers,
                                    TransactionPayRequestSerializers,
                                    TransactionPayResponseSerializers,
                                    TransactionUseRequestSerializers,
                                    TransactionUseResponseSerializers,
                                    TransactionGrantRequestSerializers,
                                    TransactionGrantResponseSerializers,
                                    TransactionSummaryRequestSerializers)
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from v1_terminal.serializers.common_serializers import (
    CommonSerializer,
    OpenApiIssueTransactionNumberSerializer,
    OpenApiTransactionChargeSerializer,
    OpenApiTransactionPaySerializer,
    OpenApiTransactionGrantSerializer,
    OpenApiTransactionUseSerializer,
    OpenApiTransactionCancelSerializer,
    OpenApiTransactionListSerializer,
    OpenApiTransactionDetailASerializer,
    OpenApiTransactionSummarySerializer
)

from v1_terminal.serializers.transaction_cancel_serializer \
    import (
        TransactionCancelRequestSerializer,
        TransactionCancelResponseSerializer
    )
from v1_terminal.serializers import (
    TransactionListRequestSerializer,
    TransactionDetailRequestSerializer)
import json

from v1_terminal.serializers.transaction_cancel_serializer \
    import (
        TransactionCancelRequestSerializer,
        TransactionCancelResponseSerializer
    )


@extend_schema(
    tags=['取引関連']
)
class TransactionAPIView(views.APIView):
    @extend_schema(
        summary="取引番号発行",
        description="事前にチャージや決済等で利用する取引番号の発行を行う",
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
        serializer = IssueTransactionNumberRequestSerializer(data=request.data)
        if serializer.is_valid():
            response_data, response_status = serializer.save()
            return Response(response_data, response_status)


@extend_schema(
    tags=['取引関連']
)
class TransactionChargeAPIView(views.APIView):
    @extend_schema(
        summary="チャージ",
        description="カードにバリューをチャージする",
        parameters=[
            OpenApiParameter("auth_token", OpenApiTypes.STR,
                             OpenApiParameter.HEADER),
            # カード番号&PIN
            OpenApiParameter("card_number", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("pin_number", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            # 磁気情報
            OpenApiParameter("magnetic_information", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            # 取引金額
            OpenApiParameter("transaction_amount", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            # 取引方式
            OpenApiParameter("transaction_method", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            # チャージ支払い方式
            OpenApiParameter("charge_method", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            # キャンペーン適用フラグ
            OpenApiParameter("apply_campaign_flag", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
        ],
        responses={
            # 未対応: 取引完了している
            200: OpenApiTransactionChargeSerializer,
            400: OpenApiResponse(
                response=CommonSerializer,
                description='異なる店舗端末からのリクエスト\t\nチャージ単位は〇〇円\t\nチャージ下限額以下\t\n1回あたりのチャージ上限額越え\t\n1日あたりのチャージ上限額超え\t\n1ヶ月あたりのチャージ上限額超え\t\n残高上限超え'),
            401: OpenApiResponse(
                response=CommonSerializer,
                description='トークン認証エラー\t\nトークン有効期限切れ'),
            403: OpenApiResponse(
                response=CommonSerializer,
                description='サービス利用許可なし\t\nアクティベートでないカード\t\nロック状態のカード'),
            404: OpenApiResponse(
                response=CommonSerializer,
                description='存在しないカード')
        }
    )
    def put(self, request, pk):
        request_data = request.data
        request_data['pk'] = pk
        serializer = TransactionChargeRequestSerializers(data=request_data)
        if serializer.is_valid():
            response, status_code = serializer.save()
            if response is not None:
                response_serializer = TransactionChargeResponseSerializers(response)
                return Response(response_serializer.data, status_code,
                                content_type='application/json')
            else:
                return Response(status=status_code)


@extend_schema(
    tags=['取引関連']
)
class TransactionPayAPIView(views.APIView):
    @extend_schema(
        summary="決済",
        description="カード決済を行う",
        parameters=[
            OpenApiParameter("auth_token", OpenApiTypes.STR,
                             OpenApiParameter.HEADER),
            OpenApiParameter(
                "cards",
                OpenApiTypes.OBJECT,
                OpenApiParameter.QUERY,
                examples=[
                    OpenApiExample(
                        'Example',
                        value=[{
                            'card_number': 'カード番号',
                            'pin_number': 'PIN番号',
                            'magnetic_information': '磁気情報',
                            'use_payable_bonus_amount': '決済併用ボーナス利用数'
                        }]
                    ),
                ]),
            # 取引金額
            OpenApiParameter("transaction_amount", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            # 取引方式
            OpenApiParameter("transaction_method", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            # キャンペーン適用フラグ
            OpenApiParameter("apply_campaign_flag", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
        ],
        responses={
            200: OpenApiTransactionPaySerializer,
            400: OpenApiResponse(
                response=CommonSerializer,
                description='異なる店舗端末からのリクエスト\t\n1回あたりの決済上限額越え\t\n1日あたりの決済上限額超え\t\n1ヶ月あたりの決済上限額超え\t\n残高超え'),
            401: OpenApiResponse(
                response=CommonSerializer,
                description='トークン認証エラー\t\nトークン有効期限切れ'),
            403: OpenApiResponse(
                response=CommonSerializer,
                description='サービス利用許可なし\t\nアクティベートでないカード\t\nロック状態のカード'),
            404: OpenApiResponse(
                response=CommonSerializer,
                description='存在しないカード')
        }
    )
    def put(self, request, pk):
        request_data = request.data
        request_data['pk'] = pk
        serializer = TransactionPayRequestSerializers(data=request_data)
        if serializer.is_valid():
            response, status_code = serializer.save()
            if response is not None:
                response_serializer = TransactionPayResponseSerializers(response)
                return Response(response_serializer.data, status_code,
                                content_type='application/json')
            else:
                return Response(status=status_code)


@extend_schema(
    tags=['取引関連']
)
class TransactionGrantAPIView(views.APIView):
    @extend_schema(
        summary="ボーナス付与",
        description="カードにボーナスを付与する",
        parameters=[
            OpenApiParameter("auth_token", OpenApiTypes.STR,
                             OpenApiParameter.HEADER),
            # カード番号&PIN
            OpenApiParameter("card_number", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("pin_number", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            # 磁気情報
            OpenApiParameter("magnetic_information", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            # 付与方法
            OpenApiParameter("grant_method", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            # 付与対象口座(前払いバリュー,決済併用ボーナス,商品交換ボーナス,etc..)
            OpenApiParameter("grant_account", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            # 取引額
            OpenApiParameter("transaction_amount", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            # 有効期限日
            OpenApiParameter("expired_at", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            # 利用制限パターン
            OpenApiParameter("usage_restriction_pattern", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            # 制限対象　企業番号
            OpenApiParameter("restricted_corporate_number", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            # 制限対象　店舗番号
            OpenApiParameter("restricted_shop_number", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            # 制限対象　管理タグ
            OpenApiParameter("restricted_management_tag", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),

        ],
        # 未対応: 取引完了している取引番号
        responses={
            200: OpenApiTransactionGrantSerializer,
            400: OpenApiResponse(
                response=CommonSerializer,
                description='存在しない取引\t\n異なる店舗端末からのリクエスト\t\n付与下限数以下\t\n1回あたりの付与上限数超え\t\n残高上限超え\t\n存在しない企業\t\n存在しない店舗\t\n存在しない管理タグ'),
            401: OpenApiResponse(
                response=CommonSerializer,
                description='トークン認証エラー\t\nトークン有効期限切れ'),
            403: OpenApiResponse(
                response=CommonSerializer,
                description='サービス利用許可なし\t\nアクティベートでないカード\t\nロック状態のカード\t\n有効でない企業\t\n有効でない店舗'),
            404: OpenApiResponse(
                response=CommonSerializer,
                description='存在しないカード')
        }
    )
    def put(self, request, pk):
        request_data = request.data
        request_data['pk'] = pk
        serializer = TransactionGrantRequestSerializers(data=request_data)
        if serializer.is_valid():
            response, status_code = serializer.save()
            if response is not None:
                response_serializer = TransactionGrantResponseSerializers(response)
                return Response(response_serializer.data, status_code,
                                content_type='application/json')
            else:
                return Response(status=status_code)


@extend_schema(
    tags=['取引関連']
)
class TransactionUseAPIView(views.APIView):
    @extend_schema(
        summary="ボーナス利用",
        description="カードで商品交換ボーナスを利用する",
        parameters=[
            OpenApiParameter("auth_token", OpenApiTypes.STR,
                             OpenApiParameter.HEADER),
            # カード番号&PIN
            OpenApiParameter("card_number", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("pin_number", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            # 磁気情報
            OpenApiParameter("magnetic_information", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            # 商品交換ボーナス利用数
            OpenApiParameter("use_exchange_bonus_amount", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
        ],
        responses={
            # 未対応: 取引完了している取引番号
            200: OpenApiTransactionUseSerializer,
            400: OpenApiResponse(
                response=CommonSerializer,
                description='存在しない取引\t\n異なる店舗端末からのリクエスト\t\n1回あたりのボーナス利用上限数超え\t\n残高上限超え'),
            401: OpenApiResponse(
                response=CommonSerializer,
                description='トークン認証エラー\t\nトークン有効期限切れ'),
            403: OpenApiResponse(
                response=CommonSerializer,
                description='サービス利用許可なし\t\nアクティベートでないカード\t\nロック状態のカード'),
            404: OpenApiResponse(
                response=CommonSerializer,
                description='存在しないカード')
        }
    )
    def put(self, request, pk):
        request_data = request.data
        request_data['pk'] = pk
        serializer = TransactionUseRequestSerializers(data=request_data)
        if serializer.is_valid():
            response, status_code = serializer.save()
            if response is not None:
                response_serializer = TransactionUseResponseSerializers(response)
                return Response(response_serializer.data, status_code,
                                content_type='application/json')
            else:
                return Response(status=status_code)


@ extend_schema(
    tags=['取引関連']
)
class TransactionCancelAPIView(views.APIView):
    @ extend_schema(
        summary="取引取消",
        description="過去に行った取引を取り消す",
        parameters=[
            OpenApiParameter("auth_token", OpenApiTypes.STR,
                             OpenApiParameter.HEADER),
            # 取引番号
            OpenApiParameter("transaction_number", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            # カード番号&PIN
            OpenApiParameter("card_number", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("pin_number", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            # 磁気情報
            OpenApiParameter("magnetic_information", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            # 取消対象取引番号
            OpenApiParameter("cancel_transaction_number", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),
        ],
        # 未対応：取引完了している取引番号
        responses={
            200: OpenApiResponse(
                response=OpenApiTransactionCancelSerializer,
                description='取消済みの取引'),
            400: OpenApiResponse(
                response=CommonSerializer,
                description='異なる店舗端末からのリクエスト\t\n存在しない取消対象取引\t\n存在しないカード\t\n残高不足\t\n残高上限超え'),
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
    def put(self, request):
        serializer = TransactionCancelRequestSerializer(data=request.data)
        if serializer.is_valid():
            transaction_cancel_response, status_code = serializer.save()
            if transaction_cancel_response is not None:
                response_serializer = TransactionCancelResponseSerializer(
                    transaction_cancel_response)
                return Response(response_serializer.data, status_code,
                                content_type='application/json')
            else:
                return Response(status=status_code)


@ extend_schema(
    tags=['取引関連']
)
class TransactionListAPIView(views.APIView):
    @ extend_schema(
        summary="取引履歴一覧取得",
        description="該当の店舗や店舗端末で実施された取引履歴の一覧を取得する",
        parameters=[
            OpenApiParameter("auth_token", OpenApiTypes.STR,
                             OpenApiParameter.HEADER),
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
            OpenApiParameter("magnetic_information", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("terminal_number", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),
            OpenApiParameter("card_number", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),
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
                description='サービス利用許可なし')
        }
    )
    def get(self, request):
        request_data = json.loads(request.body)
        serializer = TransactionListRequestSerializer(data=request_data)
        if serializer.is_valid():
            response_data, response_status = serializer.save()
            if response_data:
                return Response(response_data, response_status)
            else:
                return Response(status=response_status)


@ extend_schema(
    tags=['取引関連']
)
class TransactionDetailAPIView(views.APIView):
    @ extend_schema(
        summary="取引履歴詳細取得",
        description="取引履歴の詳細情報を取得する",
        parameters=[
            OpenApiParameter("auth_token", OpenApiTypes.STR,
                             OpenApiParameter.HEADER),
            # 取引番号
            OpenApiParameter("transaction_number", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
        ],
        # 未対応：取引完了している取引番号
        responses={
            200: OpenApiTransactionDetailASerializer,
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
    def get(self, request, pk):
        request_data = json.loads(request.body)
        # business_logic側でURIのcard_no値とrequest内のcard_no値が一致するかをチェックするため、
        # request_dataにpkの値を格納してserializerに渡す
        request_data['pk'] = pk
        serializer = TransactionDetailRequestSerializer(data=request_data)
        if serializer.is_valid():
            response_data, response_status = serializer.save()
            return Response(response_data, response_status)


@ extend_schema(
    tags=['取引関連']
)
class TransactionSummaryAPIView(views.APIView):
    @ extend_schema(
        summary="取引集計取得",
        description="取引の集計結果を取得する",
        parameters=[
            OpenApiParameter("auth_token", OpenApiTypes.STR,
                             OpenApiParameter.HEADER),
            OpenApiParameter("start_aggregation_at", OpenApiTypes.DATE,
                             OpenApiParameter.QUERY),
            OpenApiParameter("end_aggregation_at", OpenApiTypes.DATE,
                             OpenApiParameter.QUERY),
            OpenApiParameter("terminal_number", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),
        ],
        responses={
            200: OpenApiTransactionSummarySerializer,
            400: OpenApiResponse(
                response=CommonSerializer,
                description='存在しない店舗端末\t\n〇〇店の店舗端末でない'),
            401: OpenApiResponse(
                response=CommonSerializer,
                description='トークン認証エラー\t\nトークン有効期限切れ'),
            403: OpenApiResponse(
                response=CommonSerializer,
                description='サービス利用許可なし\t\n有効でない店舗端末')
        }
    )
    def get(self, request):
        request_data = json.loads(request.body)
        serializer = TransactionSummaryRequestSerializers(data=request_data)
        if serializer.is_valid():
            response_data, response_status = serializer.save()
            if response_data:
                return Response(response_data, response_status)
            else:
                return Response(status=response_status)
