from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from rest_framework import viewsets
from rest_framework.response import Response

from database.models import Company
from v1_shop.serializers import CompanySerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    ##
    # TODO: アララアカウントのみcreate操作を許可
    ##
    @extend_schema(
        responses={200: CompanySerializer},
    )
    def list(self, request):
        queryset = Company.objects.all()
        serializer = CompanySerializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        parameters=[
          CompanySerializer,  # serializer fields is converted parameters
          OpenApiParameter("nested", CompanySerializer),  # serializer object is converted parameter
          OpenApiParameter("queryparam1", OpenApiTypes.UUID, OpenApiParameter.QUERY),
          OpenApiParameter("pk", OpenApiTypes.UUID, OpenApiParameter.PATH),  # path variable was overridden
        ],
        #        request=CompanySerializer,
        responses={200: CompanySerializer},
    )
    def create(self, request):
        serializer = CompanySerializer(data=request.data)

        if serializer.is_valid():
            results = serializer.save()
            return Response(
                {
                    'status': {
                        'code': 200,
                        'message': 'success'
                    },
                    'info': {
                        'company_id': results.id,
                        'company_name': results.company_name
                    }
                }
            )
        else:
            return Response(
                {
                    'status': {
                        'code': 500,
                        'message': 'failed'
                    }
                }
            )
