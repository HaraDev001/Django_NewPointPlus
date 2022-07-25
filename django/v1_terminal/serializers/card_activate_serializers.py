from rest_framework import serializers
from ..buisiness_logic.card.card_activate import ActivateCard
from ..data.ICardActivateRepository import ICardActivateRepository
from ..data.IMockCardActivateRepository import IMockCardActivateRepository


class CardActivateRequestSerializer(serializers.Serializer):

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
        repository: ICardActivateRepository = IMockCardActivateRepository()
        activate_card = ActivateCard(repository)

        status = activate_card.execute(
            pk, card_no, card_pin, terminal_access_token
        )
        return status
