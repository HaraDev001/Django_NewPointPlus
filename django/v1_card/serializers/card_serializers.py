from rest_framework import serializers, status

from ..buisiness_logic.get_card_detail.get_card_detail import GetCardDetail
from ..data.ICardDetailRepository import ICardDetailRepository
from ..data.IMockCardDetailRepository import IMockCardDetailRepository


class CurrencyUnitSerializer(serializers.Serializer):

    prepaid_value_unit = serializers.CharField()
    payable_bonus_unit = serializers.CharField()
    product_exchange_bonus_unit = serializers.CharField()


class TransactionLimitValueSerializer(serializers.Serializer):

    value_charge_limit_for_day = serializers.IntegerField()
    value_charge_limit_for_month = serializers.IntegerField()
    value_payment_limit_for_day = serializers.IntegerField()
    value_payment_limit_for_month = serializers.IntegerField()


class TransactionResultValueSerializer(serializers.Serializer):

    value_charge_result_for_day = serializers.IntegerField(
        allow_null=True, default=0)
    value_charge_result_for_month = serializers.IntegerField(
        allow_null=True, default=0)
    value_payment_result_for_day = serializers.IntegerField(
        allow_null=True, default=0)
    value_payment_result_for_month = serializers.IntegerField(
        allow_null=True, default=0)


class CardDetailSerializer(serializers.Serializer):

    card_config_name = serializers.CharField()
    card_design = serializers.CharField()
    card_no = serializers.CharField()
    card_status = serializers.IntegerField()
    currency_unit = CurrencyUnitSerializer()
    transaction_limit_value = TransactionLimitValueSerializer()
    transaction_result_value = TransactionResultValueSerializer()


class AccessTokenCardDetailRequestSerializer(serializers.Serializer):
    access_token = serializers.CharField(required=True)
    card_no = serializers.CharField(required=True)

    def create(self, validated_data):
        repository: ICardDetailRepository = IMockCardDetailRepository()
        card_detail = GetCardDetail(repository)
        instance, response_status =\
            card_detail.execute(
                validated_data['card_no'], validated_data['access_token'])
        if response_status == status.HTTP_200_OK:
            serializer = CardDetailSerializer(instance)
            return serializer.data, response_status
        else:
            return None, response_status
