from rest_framework import serializers
from ..buisiness_logic.transaction.transaction_charge import TransactionCharge
from ..data.ICardActivateRepository import ICardActivateRepository
from ..data.IMockCardActivateRepository import IMockCardActivateRepository
from ..data.ITerminalAccessTokenRepository import ITerminalAccessTokenRepository
from ..data.IMockTerminalAccessTokenRepository import IMockTerminalAccessTokenRepository
from ..data.ITransactionChargeRepository import ITransactionChargeRepository
from ..data.IMockTransactionChargeRepository import IMockTransactionChargeRepository


class CardSerializers(serializers.Serializer):
    # カード番号
    card_no = serializers.CharField()
    # カードPIN
    card_pin = serializers.CharField()
    # 磁気情報
    magnetic_information = serializers.CharField()


class ChargeMethodSerializers(serializers.Serializer):
    # CPM
    cpm = serializers.IntegerField()
    # MPM
    mpm = serializers.IntegerField()
    # 物理
    magnetic_information = serializers.IntegerField()


class ChargeMeansSerializers(serializers.Serializer):
    # 現金
    cash = serializers.IntegerField()
    # クレジットカード
    credit_card = serializers.IntegerField()


class CampaignFlagSerializers(serializers.Serializer):
    # 同期
    sync = serializers.IntegerField()
    # 非同期
    asynchronous = serializers.IntegerField()
    # 非適用
    not_applicable = serializers.IntegerField()


class TransactionSerializer(serializers.Serializer):
    # 前払バリュー有効期限
    value_expired_at = serializers.DateTimeField()
    # 前払バリュー残高
    value_transaction_balance = serializers.IntegerField()
    # 決済併用ボーナス残高
    payable_bonus_balance = serializers.IntegerField()
    # 商品交換ボーナス残高
    product_exchange_bonus_balance = serializers.IntegerField()


class CardTransactionSerializer(serializers.Serializer):
    # カード設定名
    card_name = serializers.CharField()
    # カード番号
    card_no = serializers.CharField()
    # 取引前
    transaction_before = TransactionSerializer()
    # 取引後
    transaction_after = TransactionSerializer()


class CompanySerializer(serializers.Serializer):
    # 企業番号
    company_number = serializers.IntegerField()
    # 企業名
    company_name = serializers.CharField()


class ShopSerializer(serializers.Serializer):
    # 店舗番号
    shop_number = serializers.IntegerField()
    # 店舗名
    shop_name = serializers.CharField()


class ChargeSerializer(serializers.Serializer):
    # 対象口座
    target_account = serializers.CharField()
    # チャージ額
    charge_amount = serializers.IntegerField()


class TransactionChargeResponseSerializers(serializers.Serializer):
    # 取引種別
    transaction_type = serializers.IntegerField()
    # 取引日時
    transaction_date = serializers.DateTimeField()
    # 企業
    company = CompanySerializer()
    # 店舗
    shop = ShopSerializer()
    # 端末番号
    terminal_no = serializers.CharField()
    # チャージ
    charge = ChargeSerializer()
    # カード取引
    card_transaction = CardTransactionSerializer()


class TransactionChargeRequestSerializers(serializers.Serializer):
    # URIから取得した取引番号
    pk = serializers.CharField()
    # 認証トークン
    access_token = serializers.CharField()
    # カード
    card = CardSerializers()
    # チャージ金額
    charge_amount = serializers.IntegerField()
    # チャージ方式
    charge_method = ChargeMethodSerializers()
    # チャージ手段（現金 / クレジットカード）
    charge_means = ChargeMeansSerializers()
    # キャンペーン適用フラグ
    campaign_flag = CampaignFlagSerializers()

    def create(self, validated_data):
        pk = validated_data['pk']
        access_token = validated_data['access_token']
        card = validated_data['card']
        charge_amount = validated_data['charge_amount']
        campaign_flag = validated_data['campaign_flag']
        terminal_repository: ITerminalAccessTokenRepository = IMockTerminalAccessTokenRepository()
        card_activate_repository: ICardActivateRepository = IMockCardActivateRepository()
        transaction_charge_repository: ITransactionChargeRepository = IMockTransactionChargeRepository()
        transaction_charge = \
            TransactionCharge(card_activate_repository, terminal_repository, transaction_charge_repository)
        charge, response_status = transaction_charge.execute(pk, card, access_token, charge_amount, campaign_flag)
        return charge, response_status
