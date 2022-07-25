from django.urls import path
from .views import *


urlpatterns = [
    path('auth/token/', AuthAPIView.as_view(), name='auth'),
    path('cards/<str:card_number>/', CardAPIView.as_view(), name='card'),
    path('cards/<str:card_number>/balance/', BalanceAPIView.as_view(), name='balance'),
    path('cards/<str:card_number>/transactions/', TransactionListAPIView.as_view(), name='transactions'),
    path('cards/<str:card_number>/transactions/<str:transaction_id>/', TransactionAPIView.as_view(), name='transaction'),
    path('service/corp_info/', CorpInfoAPIView.as_view(), name='corp_info'),
]
