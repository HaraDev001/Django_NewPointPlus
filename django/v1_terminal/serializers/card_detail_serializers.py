from rest_framework import serializers, status

from ..buisiness_logic.card.get_card_detail import GetCardDetail
from ..data.ICardDetailRepository import ICardDetailRepository
from ..data.IMockCardDetailRepository import IMockCardDetailRepository


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
    transaction_limit_value = TransactionLimitValueSerializer()
    transaction_result_value = TransactionResultValueSerializer()


class GetCardDetailRequestSerializer(serializers.Serializer):

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
        repository: ICardDetailRepository = IMockCardDetailRepository()
        get_card_detail = GetCardDetail(repository)

        instance, response_status = get_card_detail.execute(
            pk, card_no, card_pin, terminal_access_token
        )
        if response_status == status.HTTP_200_OK:
            serializer = CardDetailSerializer(instance)
            return serializer.data, response_status
        else:
            return None, response_status
