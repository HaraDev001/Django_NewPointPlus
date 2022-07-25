from database.models.company import Company
from django_filters import rest_framework as filters
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework.generics import ListCreateAPIView
from v1_console.serializers import CompanySerializer
from v1_console.serializers.common_serializers import CommonSerializer, OpenApiCompanyListSerializer
from v1_console.views import ConsoleBaseView


class CompanyFilter(filters.FilterSet):
    management_tag = filters.CharFilter(field_name='management_tags', lookup_expr='name', max_length=255)
    company_name = filters.CharFilter(field_name='company_name', lookup_expr='contains', max_length=255)
    corporate_number = filters.CharFilter(field_name='corporate_number', max_length=255)
    provider_id = filters.UUIDFilter(field_name='provider_id')

    class Meta:
        model = Company
        fields = ['provider_id', 'company_name', 'corporate_number', 'management_tag', 'status']


class CompanyListAPIView(ConsoleBaseView, ListCreateAPIView):
    queryset = Company.objects.all().prefetch_related('management_tags')
    serializer_class = CompanySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CompanyFilter

    @extend_schema(
        summary="企業一覧取得",
        description="事業者に紐付く企業の一覧を取得する。",
        parameters=[
            OpenApiParameter("auth_token", OpenApiTypes.STR,
                             OpenApiParameter.HEADER),
            OpenApiParameter("provider_id", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("company_name", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("corporate_number", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            OpenApiParameter("management_tag", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
            # ステータス
            OpenApiParameter("status", OpenApiTypes.STR,
                             OpenApiParameter.QUERY),
        ],
        responses={
            200: OpenApiCompanyListSerializer,
            401: OpenApiResponse(
                response=CommonSerializer,
                description='トークン認証エラー\t\nトークン有効期限切れ'),
            403: OpenApiResponse(
                response=CommonSerializer,
                description='利用許可がないアカウント権限')
        }
    )
    def get(self, request):
        return super(CompanyListAPIView, self).get(self, request)
