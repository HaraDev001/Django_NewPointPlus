from database.models import Provider
from django_filters import rest_framework as filters
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework.generics import ListCreateAPIView
from v1_console.serializers import ProviderSerializer
from v1_console.serializers.common_serializers import CommonSerializer, OpenApiProviderListSerializer
from v1_console.views import ConsoleBaseView


class ProviderFilter(filters.FilterSet):
    provider_id = filters.UUIDFilter(field_name="id")
    provider_name = filters.CharFilter(field_name='provider_name', lookup_expr='contains', max_length=255)
    status = filters.NumberFilter(field_name='status')

    class Meta:
        model = Provider
        fields = ['provider_id', 'provider_name', 'status']


class ProviderListAPIView(ConsoleBaseView, ListCreateAPIView):
    serializer_class = ProviderSerializer
    queryset = Provider.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProviderFilter

    @extend_schema(
        summary="事業者一覧取得",
        description="事業者の一覧を取得する",
        # 認証トークン 検索（事業者ID / 事業者名 / ステータス）
        parameters=[
            OpenApiParameter("auth_token", OpenApiTypes.STR,
                             OpenApiParameter.HEADER),
            OpenApiParameter("provider_id", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("provider_name", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("status", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
        ],
        responses={
            200: OpenApiProviderListSerializer,
            401: OpenApiResponse(
                response=CommonSerializer,
                description='トークン認証エラー\t\nトークン有効期限切れ'),
            403: OpenApiResponse(
                response=CommonSerializer,
                description='利用許可がないアカウント権限')
        }
    )
    def get(self, request):
        return super(ProviderListAPIView, self).get(self, request)
