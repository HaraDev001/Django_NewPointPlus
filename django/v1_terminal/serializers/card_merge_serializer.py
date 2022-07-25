from rest_framework import serializers

from v1_terminal.data.ICardMergeRepository import ICardMergeRepository
from v1_terminal.data.IMockCardMergeRepository import IMockCardMergeRepository

from v1_terminal.buisiness_logic.card.card_merge import CardMerge


class CardMergeCardSerializer(serializers.Serializer):
    card_no_merge = serializers.CharField(required=True)
    card_pin_merge = serializers.CharField(required=True)
    card_magnetic_information = serializers.CharField()


class CardMergeRepquestSerializer(serializers.Serializer):
    terminal_access_token = serializers.CharField(required=True)
    merge_from = CardMergeCardSerializer()
    merge_to = CardMergeCardSerializer()

    def create(self, validated_data):
        repository: ICardMergeRepository = IMockCardMergeRepository()
        card_merge = CardMerge(repository)

        terminal_access_token = validated_data['terminal_access_token']
        merge_from = validated_data['merge_from']
        merge_to = validated_data['merge_to']

        card_merge_response, status = card_merge.execute(terminal_access_token, merge_from, merge_to)
        return card_merge_response, status


class CardMergeCardResponseSerializer(serializers.Serializer):
    card_config_name = serializers.CharField()
    card_no = serializers.CharField()


class CardMergeAmountResponseSerializer(serializers.Serializer):
    value_merged_amount = serializers.IntegerField()
    payable_bonus_merged_amount = serializers.IntegerField()
    product_exchage_bonus_merged_amount = serializers.IntegerField()


class CardMergeBalanceSummaryResponseSerializer(serializers.Serializer):
    card_state = serializers.IntegerField()
    value_amount = serializers.IntegerField()
    payable_bonus_amount = serializers.IntegerField()
    product_exchange_bonus_amount = serializers.IntegerField()


class CardMergeResponseSerializer(serializers.Serializer):
    source_card = CardMergeCardResponseSerializer()
    destination_card = CardMergeCardResponseSerializer()
    merged_amount = CardMergeAmountResponseSerializer()
    source_before_merge = CardMergeBalanceSummaryResponseSerializer()
    source_after_merge = CardMergeBalanceSummaryResponseSerializer()
    destination_before_merge = CardMergeBalanceSummaryResponseSerializer()
    destination_after_merge = CardMergeBalanceSummaryResponseSerializer()
