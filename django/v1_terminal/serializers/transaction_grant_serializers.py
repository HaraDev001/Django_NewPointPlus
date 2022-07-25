from rest_framework import serializers
from ..buisiness_logic.transaction.transaction_pay import TransactionPay
from ..data.ICardActivateRepository import ICardActivateRepository
from ..data.IMockCardActivateRepository import IMockCardActivateRepository
from ..data.ITerminalAccessTokenRepository import ITerminalAccessTokenRepository
from ..data.IMockTerminalAccessTokenRepository import IMockTerminalAccessTokenRepository
from ..data.ITransactionGrantRepository import ITransactionGrantRepository
from ..data.IMockTransactionGrantRepository import IMockTransactionGrantRepository


class RestrictionSubjectSerializers(serializers.Serializer):
    #企業番号
    restricted_corporate_number = serializers.CharField()
    #店舗番号
    restricted_shop_number = serializers.CharField()
    #管理タグ
    restricted_management_tags = serializers.CharField()


class UsageRestrictionSerializers(serializers.Serializer):
    #利用制限
    usage_restriction_pattern = serializers.IntegerField()
    #制限対象
    restriction_subject = RestrictionSubjectSerializers(many=True)


class CompanySerializer(serializers.Serializer):
    #企業番号
    company_number = serializers.CharField()
    #企業名
    company_name = serializers.CharField()


class ShopSerializer(serializers.Serializer):
    #店舗番号
    shop_number = serializers.CharField()
    #店舗名
    shop_name = serializers.CharField()


class GrantSerializer(serializers.Serializer):
    #付与方法
    grant_method = serializers.IntegerField()
    #対象口座
    grant_account = serializers.CharField()
    #取引額
    amount = serializers.IntegerField()


class TransactionSerializer(serializers.Serializer):
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


class TransactionGrantRequestSerializers(serializers.Serializer):
    #認証トークン
    access_token = serializers.CharField(required=True)
    #カード番号
    card_number = serializers.CharField(required=True)
    #カードPIN
    pin_number = serializers.CharField(required=True)
    # 磁気情報
    magnetic_information = serializers.CharField(required=True)
    # URIから取得したカード番号
    pk = serializers.CharField(required=True)
    #付与方法
    grant_method = serializers.IntegerField(required=True)
    #付与対象口座
    grant_account = serializers.CharField(required=True)
    #取引額
    amount = serializers.IntegerField(required=True)
    #有効期限日
    expiration_date = serializers.DateTimeField(required=True)
    # 利用制限
    usage_restriction = UsageRestrictionSerializers()

    def create(self, validated_data):
        pk = validated_data['pk']
        access_token = validated_data['access_token']
        card_number = validated_data['card_number']
        pin_number = validated_data['pin_number']
        grant_method = validated_data['grant_method']
        grant_account = validated_data['grant_account']
        amount = validated_data['amount']
        usage_restriction = validated_data['usage_restriction']
        terminal_repository: ITerminalAccessTokenRepository = IMockTerminalAccessTokenRepository()
        card_activate_repository: ICardActivateRepository = IMockCardActivateRepository()
        transaction_grant_repository: ITransactionGrantRepository = IMockTransactionGrantRepository()
        transaction_grant = \
            TransactionGrant(card_activate_repository, terminal_repository, transaction_grant_repository)
        grant, response_status = transaction_grant.execute(pk,
                                                            card_number,
                                                            pin_number,
                                                            access_token,
                                                            amount,
                                                            grant_method,
                                                            grant_account,
                                                            usage_restriction)
        return grant, response_status


class TransactionGrantResponseSerializers(serializers.Serializer):
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
    #付与
    grant = GrantSerializer()
    #カード
    card_transaction = CardTransactionSerializer()
