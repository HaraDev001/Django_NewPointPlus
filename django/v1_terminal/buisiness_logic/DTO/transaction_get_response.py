class TransactionListResponse:
    '''TransactionListResponseクラス

        取引履歴一覧を取得するGetTransactionListからSerializerへ渡されるDTOクラス

        Attributes:
            transaction_history (list型): 取引履歴一覧
    '''

    def __init__(self, transaction_history):
        self.transaction_history = transaction_history


class TransactionDetailResponse:
    '''TransactionDetailResponseクラス

        取引履歴詳細を取得するGetTransactionDetailからSerializerへ渡されるDTOクラス

    '''
    def __init__(
        self, transaction_type, transaction_at, transaction_number,
        transaction_status, company, shop, terminal, transaction, card,
        card_merge
    ):
        self.transaction_type = transaction_type
        self.transaction_at = transaction_at
        self.transaction_number = transaction_number
        self.transaction_status = transaction_status
        self.company = company
        self.shop = shop
        self.terminal = terminal
        self.transaction = transaction
        self.card = card
        self.card_merge = card_merge
