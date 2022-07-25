from rest_framework import serializers

from v1_terminal.data.ITransactionCancelRepository import ITransactionCancelRepository
from v1_terminal.data.IMockTransactionCancelRepository import IMockTransactionCancelRepository

from v1_terminal.buisiness_logic.terminal.transaction_cancel import (
    CancelTransaction
)


class TransactionCancelRequestSerializer(serializers.Serializer):
    terminal_access_token = serializers.CharField(required=True)
    transaction_id = serializers.CharField(required=True)
    cancel_transaction_id = serializers.CharField(required=True)
    card_no = serializers.CharField(required=True)
    card_pin = serializers.CharField(required=True)
    magnetic_information = serializers.CharField()

    def create(self, validated_data):
        repository: ITransactionCancelRepository = IMockTransactionCancelRepository()
        issue_access_token = CancelTransaction(repository)

        _terminal_access_token = validated_data['terminal_access_token']
        _transaction_id = validated_data['transaction_id']
        _cancel_transaction_id = validated_data['cancel_transaction_id']
        _card_no = validated_data['card_no']
        _card_pin = validated_data['card_pin']
        _magnetic_infomation = validated_data['magnetic_information']

        transaction_cancel_response, status = issue_access_token.execute(
               _terminal_access_token,
               _card_no,
               _card_pin,
               _magnetic_infomation,
               _transaction_id,
               _cancel_transaction_id)
        return transaction_cancel_response, status


class TransactionCancelCompanySerializer(serializers.Serializer):
    company_id = serializers.CharField()
    company_name = serializers.CharField()


class TransactionCancelShopSerializer(serializers.Serializer):
    shop_id = serializers.CharField()
    shop_name = serializers.CharField()


class TransactionCancelTransactionSerializer(serializers.Serializer):
    # 取引額
    transaction_amount = serializers.IntegerField()
    # 前払バリュー増減額
    value_amount = serializers.IntegerField()
    # 決済併用ボーナス増減数
    payable_bonus_amount = serializers.IntegerField()
    # 商品交換ボーナス増減数
    product_exchange_amount = serializers.IntegerField()


class TransactionCancelBalanceSerializer(serializers.Serializer):
    value_balance = serializers.IntegerField()
    value_expire_at = serializers.DateTimeField()
    payable_bonus_balance = serializers.IntegerField()
    product_exchange_bonus_balance = serializers.IntegerField()


class TransactionCancelCampaignSerializer(serializers.Serializer):
    event_name = serializers.CharField()
    cancel_grant_bank_account = serializers.CharField()
    cancel_grant_count = serializers.IntegerField()
    expire_at = serializers.DateTimeField()


class TransactionCancelCardSerializer(serializers.Serializer):
    card_config_name = serializers.CharField()
    card_no = serializers.CharField()
    # 取引前残高
    balance_before_cancel = TransactionCancelBalanceSerializer()
    # 取引後残高
    balance_after_cancel = TransactionCancelBalanceSerializer()

    # キャンペーン
    campaign = TransactionCancelCampaignSerializer(many=True)


class TransactionCancelResponseSerializer(serializers.Serializer):
    # 取消した取引種別
    transaction_type = serializers.IntegerField()
    # 取引日時
    transaction_at = serializers.DateTimeField()

    # 企業
    company = TransactionCancelCompanySerializer()
    # 店舗
    shop = TransactionCancelShopSerializer()

    # 店舗番号
    terminal_no = serializers.CharField()

    # 取引取消
    transaction_cancel = TransactionCancelTransactionSerializer()

    # カード
    card = TransactionCancelCampaignSerializer(many=True)
