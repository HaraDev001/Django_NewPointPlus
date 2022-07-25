from database.models import Permission, PermissionManagement
from database.models.common import const
from rest_framework.permissions import BasePermission

from django.contrib.auth.models import AnonymousUser

GET = "GET"
POST = "POST"
PUT = "PUT"
DELETE = "DELETE"


def _get_permission(name):
    try:
        return Permission.objects.get(name=name)
    except Permission.DoesNotExist:
        return None


def is_user_has_permission(user, permission):
    if permission is None:
        return False

    try:
        grant = PermissionManagement.objects.get(
            group=user.group,
            role=user.role,
            permission=permission
        )
    except PermissionManagement.DoesNotExist:
        return False
    else:
        if grant.state != const.MUST_REQUEST:
            return grant.state == const.ALLOW

        # In cases of MUST_REQUEST permissions, only allow to call REQUEST apis:
        return grant.permission.name in [
            const.REQUEST_CANCEL_TRANSACTION, const.WITHDRAWAL_TRANSACTION_CANCEL_REQUEST
        ]


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False
        # Otherwise, only allow authenticated requests
        return request.user


class TokenPermission(IsAuthenticated):
    def has_permission(self, request, view):
        # Allow any issue/refresh token
        if request.method in [POST, PUT]:
            return True

        # 事業者アクセストークン失効
        if request.method == DELETE:
            return is_user_has_permission(request.user, _get_permission(const.REVOKE_TOKEN))

        return super().has_permission(request, view)


# カード一覧取得
class GetCardListPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method != GET:
            return False
        return is_user_has_permission(request.user, _get_permission(const.GET_CARD_LIST))


# カード一覧CSV取得
class ExportCardCsvPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method != POST:
            return False
        return is_user_has_permission(request.user, _get_permission(const.EXPORT_CARD_CSV))


# カード詳細取得
class GetCardDetailPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method != GET:
            return False
        return is_user_has_permission(request.user, _get_permission(const.GET_CARD_DETAIL))


class TransactionPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method not in [GET, POST]:
            return False

        # 取引履歴一覧取得
        if request.method == GET:
            return is_user_has_permission(request.user, _get_permission(const.GET_TRANSACTION_HISTORY))

        # 取引番号発行
        if request.method == POST:
            return is_user_has_permission(request.user, _get_permission(const.CREATE_TRANSACTION))


# 取引履歴一覧CSV取得
class ExportTransactionCsvPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method != GET:
            return False
        return is_user_has_permission(request.user, _get_permission(const.EXPORT_TRANSACTION_CSV))


# 取引履歴詳細取得
class GetTransactionDetailPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method != GET:
            return False
        return is_user_has_permission(request.user, _get_permission(const.GET_TRANSACTION_DETAIL))


# 取引取消
class CancelTransactionPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method != PUT:
            return False
        return is_user_has_permission(request.user, _get_permission(const.CANCEL_TRANSACTION))


# 取引取消申請
class RequestCancelTransactionPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method != POST:
            return False
        return is_user_has_permission(request.user, _get_permission(const.REQUEST_CANCEL_TRANSACTION))


# 取引取消申請取下
class WithdrawalTransactionCancelRequestPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method != PUT:
            return False
        return is_user_has_permission(request.user, _get_permission(const.WITHDRAWAL_TRANSACTION_CANCEL_REQUEST))


# 取引取消承認
class ApproveCancelTransactionRequestPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method != PUT:
            return False
        return is_user_has_permission(request.user, _get_permission(const.APPROVE_CANCEL_TRANSACTION_REQUEST))


# カード取引集計取得
class GetCardSummaryPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method != GET:
            return False
        return is_user_has_permission(request.user, _get_permission(const.GET_CARD_SUMMARY))


# 基準日未使用残高集計取得
class GetBalanceSummaryPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method != GET:
            return False
        return is_user_has_permission(request.user, _get_permission(const.GET_BALANCE_SUMMARY))


# イベント別集計取得
class GetEventSummaryPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method != GET:
            return False
        return is_user_has_permission(request.user, _get_permission(const.GET_EVENT_SUMMARY))


# カード発行数集計取得
class GetIssueTotalSummaryPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method != GET:
            return False
        return is_user_has_permission(request.user, _get_permission(const.GET_ISSUE_TOTAL_SUMMARY))


# カード推移集計取得
class GetIssueTransitionSummaryPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method != GET:
            return False
        return is_user_has_permission(request.user, _get_permission(const.GET_ISSUE_TRANSITION_SUMMARY))
