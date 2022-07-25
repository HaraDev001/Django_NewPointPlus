import json

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (OpenApiParameter, OpenApiResponse,
                                   extend_schema)
from rest_framework import views
from rest_framework.response import Response
from v1_terminal.serializers import CardActivateRequestSerializer
from v1_terminal.serializers.card_merge_serializer import CardMergeRepquestSerializer
from v1_terminal.serializers.card_merge_serializer import CardMergeResponseSerializer

from v1_terminal.serializers import (CardActivateRequestSerializer,
                                     GetCardBalanceRequestSerializer,
                                     GetCardDetailRequestSerializer)
from v1_terminal.serializers.common_serializers import (
    CommonSerializer,
    OpenApiCardDetailSerializer,
    OpenApiCardBalanceSerializer,
    OpenApiCardReplaceSerializer,
)


@extend_schema(
    tags=['カード関連']
)
class CardActivateAPIView(views.APIView):
    @extend_schema(
        summary="カードアクティベート",
        description="カードをアクティベートする",
        parameters=[
            # 認証トークン
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
        ],
        responses={
            200: None,
            400: OpenApiResponse(
                response=CommonSerializer,
                description='未アクティベートでないカード'),
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
    def put(self, request, pk):
        request_data = request.data
        # business_logic側でURIのcard_no値とrequest内のcard_no値が一致するかをチェックするため、
        # request.dataにpkの値を格納してserializerに渡す
        request_data['pk'] = pk
        serializer = CardActivateRequestSerializer(data=request_data)
        if serializer.is_valid():
            status_code = serializer.save()
            return Response(status=status_code)


@extend_schema(
    tags=['カード関連']
)
class CardDetailAPIView(views.APIView):
    @extend_schema(
        summary="カード詳細取得",
        description="カードの詳細情報を取得する",
        parameters=[
            # 認証トークン
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
        ],
        responses={
            200: OpenApiResponse(
                response=OpenApiCardDetailSerializer),
            401: OpenApiResponse(
                response=CommonSerializer,
                description='トークン認証エラー\t\nトークン有効期限切れ'),
            403: OpenApiResponse(
                response=CommonSerializer,
                description='サービス利用許可なし'),
            404: OpenApiResponse(
                response=CommonSerializer,
                description='存在しないカード'),
        }
    )
    def get(self, request, pk):
        request_data = json.loads(request.body)
        # business_logic側でURIのcard_no値とrequest内のcard_no値が一致するかをチェックするため、
        # request_dataにpkの値を格納してserializerに渡す
        request_data['pk'] = pk
        serializer = GetCardDetailRequestSerializer(
            data=request_data)
        if serializer.is_valid():
            response_data, response_status = serializer.save()
            return Response(response_data, response_status)


@extend_schema(
    tags=['カード関連']
)
class CardBalanceAPIView(views.APIView):
    @extend_schema(
        summary="残高照会",
        description="カードの残高を取得する",
        parameters=[
            # 認証トークン
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
        ],
        responses={
            200: OpenApiCardBalanceSerializer,
            401: OpenApiResponse(
                response=CommonSerializer,
                description='トークン認証エラー\t\nトークン有効期限切れ'),
            403: OpenApiResponse(
                response=CommonSerializer,
                description='サービス利用許可なし'),
            404: OpenApiResponse(
                response=CommonSerializer,
                description='存在しないカード'),
        }
    )
    def get(self, request, pk):
        request_data = json.loads(request.body)
        # business_logic側でURIのcard_no値とrequest内のcard_no値が一致するかをチェックするため、
        # request_dataにpkの値を格納してserializerに渡す
        request_data['pk'] = pk
        serializer = GetCardBalanceRequestSerializer(
            data=request_data)
        if serializer.is_valid():
            response_data, response_status = serializer.save()
            return Response(response_data, response_status)


@extend_schema(
    tags=['カード関連']
)
class CardMergeAPIView(views.APIView):
    @extend_schema(
        summary="カード付替",
        description="一方のカード残高をもう一方のカード残高に統合する",
        parameters=[
            # 認証トークン
            OpenApiParameter("auth_token", OpenApiTypes.STR,
                             OpenApiParameter.HEADER),
            # 付替元カード番号&PIN
            OpenApiParameter("source_card_number", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("source_pin_number", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            # 付替元磁気情報
            OpenApiParameter("source_magnetic_information", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            # 付替先カード番号&PIN
            OpenApiParameter("target_card_number", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("target_pin_number", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            # 付替先磁気情報
            OpenApiParameter("target_magnetic_information", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
        ],
        responses={
            200: OpenApiCardReplaceSerializer,
            400: OpenApiResponse(
                response=CommonSerializer,
                description='存在しないカード(付替元)\t\n存在しないカード(付替先)'),
            401: OpenApiResponse(
                response=CommonSerializer,
                description='トークン認証エラー\t\nトークン有効期限切れ'),
            403: OpenApiResponse(
                response=CommonSerializer,
                description='サービス利用許可なし\t\nアクティベートでないカード(付替元)\t\nアクティベートでないカード(付替先)\t\nロック状態のカード(付替元)\t\nロック状態のカード(付替先)'),
            404: OpenApiResponse(
                response=CommonSerializer,
                description='存在しないカード'),
        }
    )
    def put(self, request):
        serializer = CardMergeRepquestSerializer(data=request.data)
        if serializer.is_valid():
            card_merge_response, status_code = serializer.save()
            if card_merge_response is not None:
                response_serializer = CardMergeResponseSerializer(
                    card_merge_response)
                return Response(response_serializer.data, status_code,
                                content_type='application/json')
            else:
                return Response(status=status_code)
