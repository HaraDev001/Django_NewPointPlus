from rest_framework import serializers
from ..buisiness_logic.transaction.transaction_summary import TransactionSummary
from ..data.ITerminalAccessTokenRepository import ITerminalAccessTokenRepository
from ..data.IMockTerminalAccessTokenRepository import IMockTerminalAccessTokenRepository
from ..data.ITransactionSummaryRepository import ITransactionSummaryRepository
from ..data.IMockTransactionSummaryRepository import IMockTransactionSummaryRepository


class ProductExchangeBonusSerializer(serializers.Serializer):
    #合計額
    total_amount = serializers.IntegerField()
    #合計件数
    total_number = serializers.IntegerField()
    #取消合計額
    cancal_total_amount = serializers.IntegerField()
    #取消合計件数
    cancel_total_number = serializers.IntegerField()


class UseBonusSerializer(serializers.Serializer):
    #商品交換ボーナス
    product_exchange_bonus = ProductExchangeBonusSerializer()


class GrantPayableBonusSerializer(serializers.Serializer):
    #合計額
    total_amount = serializers.IntegerField()
    #合計件数
    total_number = serializers.IntegerField()
    #取消合計額
    cancal_total_amount = serializers.IntegerField()
    #取消合計件数
    cancel_total_number = serializers.IntegerField()


class GrantBonusSerializer(serializers.Serializer):
    #決済併用ボーナス
    grant_payable_bonus = GrantPayableBonusSerializer()
    #商品交換ボーナス
    product_exchange_bonus = ProductExchangeBonusSerializer()

class PayableBonusSerializer(serializers.Serializer):
    #合計額
    total_amount = serializers.IntegerField()
    #取消合計額
    cancal_total_amount = serializers.IntegerField()


class PrepaidValueSerializer(serializers.Serializer):
    #合計額
    total_amount = serializers.IntegerField()
    #取消合計額
    cancal_total_amount = serializers.IntegerField()


class PaymentSerializer(serializers.Serializer):
    #合計額
    total_amount = serializers.IntegerField()
    #合計件数
    total_number = serializers.IntegerField()
    #取消合計額
    cancal_total_amount = serializers.IntegerField()
    #取消合計件数
    cancel_total_number = serializers.IntegerField()
    #前払バリュー
    prepaid_value = PrepaidValueSerializer()
    #決済併用ボーナス
    payable_bonus = PayableBonusSerializer()

class ChargeSerializer(serializers.Serializer):
    #合計額
    total_amount = serializers.IntegerField()
    #合計件数
    total_number = serializers.IntegerField()
    #取消合計額
    cancal_total_amount = serializers.IntegerField()
    #取消合計件数
    cancel_total_number = serializers.IntegerField()


class SearchDateSerializer(serializers.Serializer):
    #開始日時
    start_aggregation_at = serializers.DateField()
    #終了日時
    end_aggregation_at = serializers.DateField()


class SearchSerializer(serializers.Serializer):
    #検索日時
    search_date = SearchDateSerializer()
    #端末番号
    terminal_number = serializers.IntegerField()


class TransactionSummaryRequestSerializers(serializers.Serializer):
    #認証トークン
    access_token = serializers.CharField()
    #検索
    search = SearchSerializer()

    def create(self, validated_data):
        access_token = validated_data['access_token']
        search = validated_data['search']
        terminal_repository: ITerminalAccessTokenRepository = IMockTerminalAccessTokenRepository()
        transaction_summary_repository: ITransactionSummaryRepository = IMockTransactionSummaryRepository()
        transaction_summary = \
            TransactionSummary(terminal_repository, transaction_summary_repository)
        summary, response_status = transaction_summary.execute(access_token, search)
        return summary, response_status


class TransactionSummaryResponseSerializers(serializers.Serializer):
    #チャージ
    charge = ChargeSerializer()
    #決済
    payment = PaymentSerializer()
    #ボーナス付与
    grant = GrantBonusSerializer()
    #ボーナス利用
    use = UseBonusSerializer()
