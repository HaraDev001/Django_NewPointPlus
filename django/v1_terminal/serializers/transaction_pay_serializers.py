from rest_framework import serializers
from ..buisiness_logic.transaction.transaction_pay import TransactionPay
from ..data.ICardActivateRepository import ICardActivateRepository
from ..data.IMockCardActivateRepository import IMockCardActivateRepository
from ..data.ITerminalAccessTokenRepository import ITerminalAccessTokenRepository
from ..data.IMockTerminalAccessTokenRepository import IMockTerminalAccessTokenRepository
from ..data.ITransactionPayRepository import ITransactionPayRepository
from ..data.IMockTransactionPayRepository import IMockTransactionPayRepository


class UsedPaymentBonusSerializers(serializers.Serializer):
    #決済併用ボーナス利用数
    used_payment_bonus_number = serializers.IntegerField()


class CardSerializers(serializers.Serializer):
    #カード番号
    card_no = serializers.CharField()
    #カードPIN
    card_pin = serializers.CharField()
    # 磁気情報
    magnetic_information = serializers.CharField()
    #利用ボーナス（決済併用ボーナス利用数）
    used_payment_bonus = UsedPaymentBonusSerializers()

class PayMethodSerializers(serializers.Serializer):
    #CPM
    cpm = serializers.IntegerField()
    #MPM
    mpm = serializers.IntegerField()
    # 物理
    magnetic_information = serializers.IntegerField()


class CampaignFlagSerializers(serializers.Serializer):
    #同期
    sync = serializers.IntegerField()
    #非同期
    asynchronous = serializers.IntegerField()
    #非適用
    not_applicable = serializers.IntegerField()


class CompanySerializer(serializers.Serializer):
    #企業番号
    company_number = serializers.IntegerField()
    #企業名
    company_name = serializers.CharField()


class ShopSerializer(serializers.Serializer):
    #店舗番号
    shop_number = serializers.IntegerField()
    #店舗名
    shop_name = serializers.CharField()


class PaymentSerializer(serializers.Serializer):
    #決済額
    payment_amount = serializers.IntegerField()
    #前払バリュー利用額
    prepaid_value = serializers.IntegerField()
    #決済併用ボーナス利用数
    payable_bonus = serializers.IntegerField()


class TransactionSerializer(serializers.Serializer):
    #前払バリュー有効期限
    value_expired_at = serializers.DateTimeField()
    #前払バリュー残高
    value_transaction_balance = serializers.IntegerField()
    #決済併用ボーナス残高
    payable_bonus_balance = serializers.IntegerField()
    #商品交換ボーナス残高
    product_exchange_bonus_balance = serializers.IntegerField()


class CampaignSerializer(serializers.Serializer):
    #キャンペーン名
    campaign_name = serializers.CharField()
    #付与対象口座
    account_to_granted = serializers.CharField()
    #付与数
    grant_amount = serializers.IntegerField()
    #有効期限日
    expired_at = serializers.DateTimeField()
    #付与予定日
    grant_schedule_at = serializers.DateTimeField()


class CardTransactionSerializer(serializers.Serializer):
    #カード設定名
    card_name = serializers.CharField()
    #カード番号
    card_no = serializers.CharField()
    #取引前
    transaction_before = TransactionSerializer()
    #取引後
    transaction_after = TransactionSerializer()
    #キャンペーン
    campaign = CampaignSerializer(many=True)


class TransactionPayRequestSerializers(serializers.Serializer):
    #URIから取得した取引番号
    pk = serializers.CharField()
    #認証トークン
    access_token = serializers.CharField()
    #カード
    card = serializers.ListField(
        child=CardSerializers()
    )
    #決済額
    payment_amount = serializers.IntegerField()
    #決済方式
    pay_method = PayMethodSerializers()
    #キャンペーン適用フラグ
    campaign_flag = CampaignFlagSerializers()

    def create(self, validated_data):
        pk = validated_data['pk']
        access_token = validated_data['access_token']
        card = validated_data['card']
        payment_amount = validated_data['payment_amount']
        campaign_flag = validated_data['campaign_flag']
        terminal_repository: ITerminalAccessTokenRepository = IMockTerminalAccessTokenRepository()
        card_activate_repository: ICardActivateRepository = IMockCardActivateRepository()
        transaction_pay_repository: ITransactionPayRepository = IMockTransactionPayRepository()
        transaction_pay = \
            TransactionPay(card_activate_repository, terminal_repository, transaction_pay_repository)
        pay, response_status = transaction_pay.execute(pk, card, access_token, charge_amount, campaign_flag)
        return pay, response_status


class TransactionPayResponseSerializers(serializers.Serializer):
     #取引種別
    transaction_type = serializers.IntegerField()
    #取引日時
    transaction_date = serializers.DateTimeField()
    #企業
    company = CompanySerializer()
    #店舗
    shop = ShopSerializer()
    #端末番号
    terminal_no = serializers.CharField()
    #決済
    payment = PaymentSerializer()
    #カード
    card_transaction = CardTransactionSerializer(many=True)
