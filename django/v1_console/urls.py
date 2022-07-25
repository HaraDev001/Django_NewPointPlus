from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from v1_console.views import *


urlpatterns = [
    # 認証系
    path('auth/token/', AuthAPIView.as_view(), name="auth_token"),

    # アカウント系
    path('accounts/password/set', SetPasswordAPIView.as_view(), name="account_set_password"),
    path('accounts/operations/permissions/', OperationPermissionListAPIView.as_view(),
         name="account_operation_permission_list"),

    # カード系
    path('cards/', CardListAPIView.as_view(), name="card_list"),
    path('cards/{pk}/', CardDetailAPIView.as_view(), name="card_detail"),
    path('cards/csv/', CardListCsvAPIView.as_view(), name="card_list_csv"),


    # 事業者系
    path('providers/', ProviderListAPIView.as_view(), name="provider_list"),

    # 企業系
    path('companies/', CompanyListAPIView.as_view(), name="company_list"),

    # 店舗系
    path('shops/', ShopListAPIView.as_view(), name="shop_list"),

    # 店舗端末系
    path('terminals/', TerminalListAPIView.as_view(), name="terminal_list"),

    # 取引履歴系
    path('transactions/', TransactionListAPIView.as_view(), name="transaction_list"),
    path('transactions/csv/', TransactionListCsvAPIView.as_view(), name="transaction_list_csv"),
    path('transactions/{id}/', TransactionDetailAPIView.as_view(), name="transaction_detail"),
    path('transactions/type/', TransactionTypeListAPIView.as_view(), name="transaction_type_list"),
    path('transactions/{id}/cancel/', TransactionCancelAPIView.as_view(), name="transaction_cancel"),
    path('transactions/{id}/cancel/requests/',
         TransactionCancelRequestAPIView.as_view(), name="transaction_cancel_request"),
    path('transactions/{id}/cancel/requests/{id}', TransactionCancelRequestApproveAPIView.as_view(),
         name="transaction_cancel_request_approve"),
    path('transactions/{id}/cancel/requests/{id}/withdrawal',
         TransactionCancelRequestWithdrawalAPIView.as_view(), name="transaction_cancel_request_withdrawal"),

    # 集計系
    path('summary/card/', CardTransactionSummaryAPIView.as_view(), name="card_summary"),
    path('summary/event/', EventSummaryAPIView.as_view(), name="event_summary"),
    path('summary/balance/', BalanceSummaryAPIView.as_view(), name="balance_summary"),
    path('summary/issue/transition', CardIssueTransitionSummaryAPIView.as_view(), name="card_issue_transition_summary"),
    path('summary/issue/total/', CardIssueTotalSummaryAPIView.as_view(), name="card_issue_total_summary"),
    path('summary/issue/transition/', CardIssueTransitionSummaryAPIView.as_view(), name="card_issue_transaction_summary"),


    # 申請取得系
    path('requests/', RequestListAPIView.as_view(), name="request_list"),
    path('requests/transactions/cancel/{pk}', TransactionCancelRequestDetailAPIView.as_view(),
         name="transaction_cancel_request_detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
