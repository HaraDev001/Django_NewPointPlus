class TransactionNumberIssueResponse:
    '''TransactionNumberIssueResponseクラス

        取引番号を発行するIssueTransactionNumberからSerializerへ渡されるDTOクラス

        Attributes:
            transaction_number (str型): 取引番号.
    '''

    def __init__(self, transaction_number):
        self.transaction_number = transaction_number
