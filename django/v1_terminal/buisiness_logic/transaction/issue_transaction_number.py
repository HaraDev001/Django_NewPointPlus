from rest_framework import status
from utils.datetime_utility import now, to_utc_timestamp
from v1_terminal.data.IIssueTransactionNumberReposiotry import \
    IIssueTransactionNumberRepository

from ..DTO.transaction_number_issue_response import \
    TransactionNumberIssueResponse


class IssueTransactionNumber:
    '''
        IssueTransactionNumberクラス

        Attributes:
            issue_transaction_number_repository(IIssueTransactionNumberRepository型):
            IIssueTransactionNumberRepositoryを継承したオブジェクト
    '''

    def __init__(
        self,
        issue_transaction_number_repository: IIssueTransactionNumberRepository,
    ):
        self.issue_transaction_number_repository:\
            IIssueTransactionNumberRepository =\
            issue_transaction_number_repository

    def execute(self, terminal_access_token):
        '''
            取引番号を発行する。
            1. requestから渡される認証トークンを元に、店舗端末認証情報を取得する。
            2. 項目チェックを実行する。
            3. 取引番号を発行する。
            4. Serializerに渡すためのinstanceと、ステータスコードを返す。

            Args:
                terminal_access_token(str): 認証トークン

            Returns:
                TransactionNumberIssueResponse型
                int型: HTTPステータスコード

        '''

        try:
            terminal_authorization = self.issue_transaction_number_repository.\
                get_terminal_authorization_by_access_token(
                    terminal_access_token)
        except Exception:
            # トークン認証エラー
            # リクエストされたトークンを保持する店舗端末認証情報がない
            return None, status.HTTP_200_OK

        # トークン有効期限切れ
        current_unixtime = int(to_utc_timestamp(now()))
        if current_unixtime > terminal_authorization.access_token_expires_at:
            return None, status.HTTP_400_BAD_REQUEST

        # 取引番号発行
        transaction_number = self.issue_transaction_number_repository.\
            issue_transaction_number()

        # 取引履歴レコード作成
        # 現状は発行した取引番号でのレコードを作成する。
        # モデル定義後変更の可能性あり。
        self.issue_transaction_number_repository.create_transaction(
            transaction_number)

        return TransactionNumberIssueResponse(transaction_number),\
            status.HTTP_200_OK
