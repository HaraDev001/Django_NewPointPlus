from rest_framework import serializers
from ..buisiness_logic.transaction.transaction_use import TransactionUse
from ..data.ICardActivateRepository import ICardActivateRepository
from ..data.IMockCardActivateRepository import IMockCardActivateRepository
from ..data.ITerminalAccessTokenRepository import ITerminalAccessTokenRepository
from ..data.IMockTerminalAccessTokenRepository import IMockTerminalAccessTokenRepository
from ..data.ITransactionUseRepository import ITransactionUseRepository
from ..data.IMockTransactionUseRepository import IMockTransactionUseRepository


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


class CardSerializers(serializers.Serializer):
    #カード番号
    card_no = serializers.CharField()
    #カードPIN
    card_pin = serializers.CharField()
    # 磁気情報
    magnetic_information = serializers.CharField()
    #決済併用ボーナス利用数
    product_exchange_bonus_used_number = serializers.IntegerField()


class UseBonusSerializer(serializers.Serializer):
    #対象口座
    account = serializers.CharField()
    #ボーナス利用数
    product_exchange_bonus = serializers.IntegerField()


class TransactionSerializer(serializers.Serializer):
    #商品交換ボーナス残高
    product_exchange_bonus_balance = serializers.IntegerField()


class CardTransactionSerializer(serializers.Serializer):
    #カード設定名
    card_name = serializers.CharField()
    #カード番号
    card_no = serializers.CharField()
    #取引前
    transaction_before = TransactionSerializer()
    #取引後
    transaction_after = TransactionSerializer()


class TransactionUseRequestSerializers(serializers.Serializer):
    #URIから取得した取引番号
    pk = serializers.CharField()
    #認証トークン
    access_token = serializers.CharField()
    #カード
    card = CardSerializers(many=True)

    def create(self, validated_data):
        pk = validated_data['pk']
        access_token = validated_data['access_token']
        card = validated_data['card']
        terminal_repository: ITerminalAccessTokenRepository = IMockTerminalAccessTokenRepository()
        card_activate_repository: ICardActivateRepository = IMockCardActivateRepository()
        transaction_use_repository: ITransactionUseRepository = IMockTransactionUseRepository(pk)
        transaction_use = \
            TransactionUse(card_activate_repository, terminal_repository, transaction_use_repository)
        use, response_status = transaction_pay.execute(pk, card, access_token)
        return use, response_status


class TransactionUseResponseSerializers(serializers.Serializer):
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
    #ボーナス利用
    use_bonus = UseBonusSerializer()
    #カード
    card_transaction = CardTransactionSerializer(many=True)