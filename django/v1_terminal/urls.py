from django.urls import path
from .views import *

urlpatterns = [
    # トークン
    path('token/', TokenAPIView.as_view(), name="token"),
    # カード
    path('cards/<pk>/activate/', CardActivateAPIView.as_view(), name="card_activate"),
    path('cards/<pk>/', CardDetailAPIView.as_view(), name="card_detail"),
    path('cards/<pk>/balance/', CardBalanceAPIView.as_view(), name="balance"),
    path('cards/<pk>/merge/', CardMergeAPIView.as_view(), name="merge"),
    # 取引
    # パスが重複していたためコメントアウト
    # path('transactions/', TransactionAPIView.as_view(), name="transaction"),
    path('transactions/<pk>/charge/', TransactionChargeAPIView.as_view(), name="charge"),
    path('transactions/<pk>/pay/', TransactionPayAPIView.as_view(), name="pay"),
    path('transactions/<pk>/grant/', TransactionGrantAPIView.as_view(), name="grant"),
    path('transactions/<pk>/use/', TransactionUseAPIView.as_view(), name="use"),
    path('transactions/<pk>/cancel/', TransactionCancelAPIView.as_view(), name="cancel"),
    path('transactions/', TransactionListAPIView.as_view(), name="list"),
    path('transactions/<pk>/', TransactionDetailAPIView.as_view(), name="transaction_detail"),
    path('transactions/summary/', TransactionSummaryAPIView.as_view(), name="summary"),
]
