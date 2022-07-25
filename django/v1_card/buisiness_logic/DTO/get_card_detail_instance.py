class GetCardDetailInstance:
    '''
    GetCardDetailInstanceクラス
    GetCardDetailからCardDetailSerializerに渡すためのインスタンスを作成するクラス
    '''
    def __init__(
        self, card_config_name, card_design, card_no, card_status,
        currency_unit, transaction_limit_value, transaction_result_value
    ):
        self.card_config_name = card_config_name
        self.card_design = card_design
        self.card_no = card_no
        self.card_status = card_status
        self.currency_unit = currency_unit
        self.transaction_limit_value = transaction_limit_value
        self.transaction_result_value = transaction_result_value
