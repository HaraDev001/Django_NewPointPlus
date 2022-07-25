from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from v1_shop.views import *

company_list = CompanyViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

urlpatterns = [
    path('companies/', company_list, name="companies"),
    path('accounting_history/<pk>/', AccountingHistoryRerieveView.as_view(), name='accounting_history_views')
]
urlpatterns = format_suffix_patterns(urlpatterns)
