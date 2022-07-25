from rest_framework import serializers, status

from ..buisiness_logic.transaction.get_transaction_detail import \
    GetTransactionDetail
from ..buisiness_logic.transaction.get_transaction_list import \
    GetTransactionList
from ..data.IMockTransactionGetRepository import IMockTransactionGetRepository
from ..data.ITransactionGetRepository import ITransactionGetRepository
from .transaction_get_response_serializers import (
    TransactionResponseListSerializer, TransactionResponseSerializer)


class TransactionDateRequestSerializer(serializers.Serializer):
    # 取引取得開始日時
    transaction_start = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        input_formats=["%Y-%m-%d %H:%M:%S"],
        required=False, allow_null=True
        )
    # 取引取得終了日時
    transaction_end = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        input_formats=["%Y-%m-%d %H:%M:%S"],
        required=False, allow_null=True
        )


class SearchCriteriaSerializer(serializers.Serializer):
    # 取引種別
    transaction_type = serializers.IntegerField(required=False, allow_null=True)
    # 取引取得日時
    transaction_date = TransactionDateRequestSerializer(required=False, allow_null=True)
    # 取引状態
    transaction_status = serializers.IntegerField(required=False, allow_null=True)
    # 端末番号
    terminal_no = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    # カード番号
    card_no = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    # 磁気情報
    magnetic_information = serializers.CharField(required=False, allow_null=True, allow_blank=True)


class SortOrderSerializer(serializers.Serializer):
    # 取引日時
    transaction_at = serializers.ChoiceField(['asc', 'desc'], required=False, allow_null=True, allow_blank=True)


class TransactionListRequestSerializer(serializers.Serializer):
    # トークン
    access_token = serializers.CharField(required=True)
    # 開始位置
    start_index = serializers.IntegerField(required=True)
    # 取得件数
    item_number = serializers.IntegerField(required=True)
    # 検索
    search_criteria = SearchCriteriaSerializer(required=False)
    # 並び順
    sort_order = SortOrderSerializer(required=False)

    def create(self, validated_data):
        terminal_access_token = validated_data['access_token']
        start_index = validated_data['start_index']
        item_number = validated_data['item_number']

        # 検索条件
        search_criteria = validated_data.get('search_criteria')
        # 検索条件の中身の取得。
        # 指定がないものはNoneで設定するためにdict.get()を使用する。
        if search_criteria:
            transaction_type = search_criteria.get('transaction_type')
            transaction_date = search_criteria.get('transaction_date')
            transaction_start = transaction_date.get('transaction_start')
            transaction_end = transaction_date.get('transaction_end')
            transaction_status = search_criteria.get('transaction_status')
            terminal_no = search_criteria.get('terminal_no')
            card_no = search_criteria.get('card_no')
            magnetic_information = search_criteria.get('magnetic_information')
        else:
            transaction_type = None
            transaction_date = None
            transaction_start = None
            transaction_end = None
            transaction_status = None
            terminal_no = None
            card_no = None
            magnetic_information = None

        # 並び順の指定
        sort_order_dict = validated_data.get('sort_order')
        if sort_order_dict:
            sort_order = sort_order_dict.get('transaction_at')
        else:
            sort_order = None

        transaction_repository: ITransactionGetRepository = IMockTransactionGetRepository()
        transaction_list = GetTransactionList(transaction_repository)
        instance_list, response_status = transaction_list.execute(
            terminal_access_token, transaction_type, transaction_start, transaction_end, transaction_status,
            terminal_no, card_no, magnetic_information)
        if instance_list:
            sorted_instance = transaction_list.execute_sort(instance_list, start_index, item_number, sort_order)
        else:
            sorted_instance = None
        if response_status == status.HTTP_200_OK:
            response_serializer = TransactionResponseListSerializer(instance=sorted_instance)
            return response_serializer.data, response_status
        else:
            return None, response_status


class TransactionDetailRequestSerializer(serializers.Serializer):
    access_token = serializers.CharField(required=True)
    transaction_number = serializers.IntegerField(required=True)
    pk = serializers.IntegerField(required=True)

    def create(self, validated_data):
        terminal_access_token = validated_data['access_token']
        transaction_number = validated_data['transaction_number']
        pk = validated_data['pk']
        transaction_repository: ITransactionGetRepository = IMockTransactionGetRepository()
        transaction_detail = GetTransactionDetail(transaction_repository)

        transaction_instance, response_status = transaction_detail.execute(
                terminal_access_token, transaction_number, pk
        )
        if response_status == status.HTTP_200_OK:
            response_serializer = TransactionResponseSerializer(instance=transaction_instance)
            return response_serializer.data, response_status
        return None, response_status
