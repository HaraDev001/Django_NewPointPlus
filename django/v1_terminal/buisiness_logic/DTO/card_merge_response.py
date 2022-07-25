
class CardMergeCard:

    def __init__(self, card_config_name, card_no):
        self.card_config_name = card_config_name
        self.card_no = card_no


class CardMergeAmount:
    def __init__(self, value_merged_amount, payable_bonus_merged_amount, product_exchage_bonus_merged_amount):
        self.value_merged_amount = value_merged_amount
        self.payable_bonus_merged_amount = payable_bonus_merged_amount
        self.product_exchage_bonus_merged_amount = product_exchage_bonus_merged_amount


class CardMergeBalanceSummary:

    def __init__(self,
                 card_state,
                 value_amount, payable_bonus_amount, product_exchage_bonus_amount):
        self.card_state = card_state
        self.value_amount = value_amount
        self.payable_bonus_amount = payable_bonus_amount
        self.product_exchange_bonus_amount = product_exchage_bonus_amount


class CardMergeResponse:
    '''CardMergeResponseクラス

        カード付替を実行するCardMergeクラスからSerializerへ渡されるDTOクラス

        Attributes:
            source_card (CardMergeCard型):付替元カードの情報
            destination_card (CardMergeCard型):付替先カードの情報
            merged_amount (CardMergeAmount型): 付け替えた残高
            source_before_merge (CardMergeBalanceSummary型): 付替前の付替元の残高.
            source_after_merge (CardMergeBalanceSummary型): 付替後の付替元の残高.
            destination_before_merge (CardMergeBalanceSummary型): 付替前の付替先の残高.
            destination_after_merge (CardMergeBalanceSummary型): 付替後の付替先の残高.
    '''

    def __init__(
                 self,
                 source_card, destination_card,
                 merged_amount,
                 source_before_merge, source_after_merge,
                 destination_before_merge, destination_after_merge):

        self.source_card = source_card,
        self.destination_card = destination_card
        self.merged_amount = merged_amount
        self.source_before_merge = source_before_merge
        self.source_after_merge = source_after_merge
        self.destination_before_merge = destination_before_merge
        self.destination_after_merge = destination_after_merge
