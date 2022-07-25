from v1_terminal.data.ITransactionSummaryRepository import ITransactionSummaryRepository
from v1_terminal.data.ITerminalAccessTokenRepository import ITerminalAccessTokenRepository
from v1_terminal.buisiness_logic.access_token.evaluate_access_token \
    import EvaluateAccessToken
from v1_terminal.buisiness_logic.access_token.common \
    import decode_token_to_json

from rest_framework import status

class TransactionSummary:
    '''
        TransactionSummaryクラス

        Attributes:
            access_token_repository(ITerminalAccessTokenRepository型):
            ITerminalAccessTokenRepositoryを継承したオブジェクト
            transaction_summary_repository(ITransactionSummaryRepository型):
            ITransactionSummaryRepositoryを継承したオブジェクト
    '''

    def __init__(
        self, access_token_repository: ITerminalAccessTokenRepository,
        transaction_summary_repository: ITransactionSummaryRepository,
    ):
        self.access_token_repository: ITerminalAccessTokenRepository =\
            access_token_repository

        self.transaction_summary_repository: ITransactionSummaryRepository =\
            transaction_summary_repository


    def execute(self, access_token, search):
        '''
        取引集計情報取得処理

        Attributes:
            access_token(str): 認証情報
            search(dict): 取引検索
        '''

        evalueate_access_token = EvaluateAccessToken(self.access_token_repository)
        principal_id = evalueate_access_token.execute(access_token)

        if not principal_id:
            return None, status.HTTP_200_OK

        access_token_payload_json = decode_token_to_json(access_token)
        terminal_no = access_token_payload_json['terminal_no']

        #端末番号が異なる
        if search['terminal_number'] != terminal_no:
            return None, status.HTTP_400_BAD_REQUEST

        summary = self.transaction_summary_repository.summary(search)

        if not summary:
            return None, status.HTTP_400_BAD_REQUEST

        else:
            return summary, status.HTTP_200_OK,