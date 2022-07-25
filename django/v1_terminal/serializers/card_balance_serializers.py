from rest_framework import serializers, status

from ..buisiness_logic.card.get_card_balance import GetCardBalance
from ..data.ICardBalanceRepository import ICardBalanceRepository
from ..data.ICardDetailRepository import ICardDetailRepository
from ..data.IMockCardBalanceRepository import IMockCardBalanceRepository
from ..data.IMockCardDetailRepository import IMockCardDetailRepository


class CompanySerializer(serializers.Serializer):

    company_number = serializers.IntegerField()
    company_name = serializers.CharField()


class ShopSerializer(serializers.Serializer):

    shop_number = serializers.IntegerField()
    shop_name = serializers.CharField()


class UsageLimitTargetSerializer(serializers.Serializer):

    company = CompanySerializer(many=True)
    shop = ShopSerializer(many=True)


class BalancebyUsageLimitserializer(serializers.Serializer):

    usage_limit_pattern = serializers.IntegerField()
    target = UsageLimitTargetSerializer()
    balance = serializers.IntegerField()


class BalancebyExpirationSerializer(serializers.Serializer):

    expires_at = serializers.DateField()
    balance = serializers.IntegerField()


class ToBeGrantedBalanceSerializer(serializers.Serializer):

    to_be_granted_at = serializers.DateField()
    balance = serializers.IntegerField()


class PrepaidValueBalanceSerializer(serializers.Serializer):

    total_balance = serializers.IntegerField()
    balance_by_usage_limit = BalancebyUsageLimitserializer(many=True)
    balance_by_expiration = BalancebyExpirationSerializer(many=True)
    to_be_granted_balance = ToBeGrantedBalanceSerializer(many=True)


class PayableBonusBalanceSerializer(serializers.Serializer):

    total_balance = serializers.IntegerField()
    balance_by_usage_limit = BalancebyUsageLimitserializer(many=True)
    balance_by_expiration = BalancebyExpirationSerializer(many=True)
    to_be_granted_balance = ToBeGrantedBalanceSerializer(many=True)


class ProductExchangeBonusBalanceSerializer(serializers.Serializer):

    total_balance = serializers.IntegerField()
    balance_by_usage_limit = BalancebyUsageLimitserializer(many=True)
    balance_by_expiration = BalancebyExpirationSerializer(many=True)
    to_be_granted_balance = ToBeGrantedBalanceSerializer(many=True)


class CardBalanceSerializer(serializers.Serializer):

    total_balance = serializers.IntegerField()
    prepaid_value = PrepaidValueBalanceSerializer()
    payable_bonus = PayableBonusBalanceSerializer()
    product_exchange_bonus = ProductExchangeBonusBalanceSerializer()


class GetCardBalanceRequestSerializer(serializers.Serializer):

    access_token = serializers.CharField(required=True)
    card_no = serializers.CharField(required=True)
    card_pin = serializers.CharField(required=True)
    # 磁気情報
    # 現行のAPI仕様書では使用用途なしだが、フェーズ2で使用する可能性あり
    magnetic_information = serializers.CharField(required=True)
    # URIから取得したカード番号
    pk = serializers.CharField(required=True)

    def create(self, validated_data):

        card_no = validated_data['card_no']
        card_pin = validated_data['card_pin']
        terminal_access_token = validated_data['access_token']
        pk = validated_data['pk']
        card_detail_repository: ICardDetailRepository =\
            IMockCardDetailRepository()
        card_balance_repository: ICardBalanceRepository =\
            IMockCardBalanceRepository()
        card_balance = GetCardBalance(
            card_detail_repository, card_balance_repository)
        instance, response_status =\
            card_balance.execute(
                pk, card_no, card_pin, terminal_access_token)
        if response_status == status.HTTP_200_OK:
            serializer = CardBalanceSerializer(instance)
            return serializer.data, response_status
        else:
            return None, response_status
