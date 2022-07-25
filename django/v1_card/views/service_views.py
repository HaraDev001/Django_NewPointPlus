from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import views, status
from rest_framework.response import Response
from ..serializers.corp_info_serializers import CorpInfoRequestSerializer

from v1_card.serializers.common_serializers import (
    CommonSerializer,
    OpenApiInformationSerializer
)


@extend_schema(
    tags=['サービス関連']
)
class CorpInfoAPIView(views.APIView):
    @extend_schema(
        summary='サービス情報取得API',
        description='事業者に紐づくWeb UI上の画面表示項目のうち、ユーザーに直接紐付かない事業者及びサービス情報を返す。',
        responses={
            200: OpenApiInformationSerializer,
            400: OpenApiResponse(
                response=CommonSerializer,
                description='未設定のHost\t\n存在しないドメイン名')
        }
    )
    def get(self, request):
        # ヘッダー取得からホスト取得
        request_data = {'host': request.META.get('HTTP_HOST')}
        serializer = CorpInfoRequestSerializer(data=request_data)
        if serializer.is_valid():
            response_data, response_status = serializer.save()
            return Response(response_data, response_status)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
