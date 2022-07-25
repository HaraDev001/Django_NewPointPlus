class GetCardBalanceInstance:
    '''
    GetCardBalanceInstanceクラス
    GetCardBalanceからCardBalanceSerializerに渡すためのインスタンスを作成するクラス
    '''
    def __init__(
        self, total_balance, prepaid_value, payable_bonus,
        product_exchange_bonus
    ):
        self.total_balance = total_balance
        self.prepaid_value = prepaid_value
        self.payable_bonus = payable_bonus
        self.product_exchange_bonus = product_exchange_bonus
