from datetime import datetime
from unittest import mock
from uuid import uuid4

from utils.datetime_utility import to_utc_timestamp

from .IIssueTransactionNumberReposiotry import \
    IIssueTransactionNumberRepository


class IMockIssueTransactionnNumberRepository(
    IIssueTransactionNumberRepository
):
    '''
    IIssueTransactionNumberRepositoryを実装したクラス

        IIssueTransactionNumberRepositoryを実装したモックオブジェクトを扱うクラス

        Attributes:
            terminal_authorizations (dict): 店舗端末認証情報を保持
            transactions(dict): 取引履歴情報を保持
    '''

    def __init__(self):

        self.terminal_authorizations = dict()
        self.transactions = dict()

        # 店舗端末認証情報
        terminal_authorization_1 = mock.MagicMock(
            terminal_no='1',
            access_token='header.payload.terminal_1',
            access_token_expires_at=to_utc_timestamp(
                datetime(2025, 7, 31, 12, 0, 0))
        )
        terminal_authorization_2 = mock.MagicMock(
            terminal_no='2',
            access_token='header.payload.terminal_2',
            access_token_expires_at=to_utc_timestamp(
                datetime(2021, 7, 1, 12, 0, 0))
        )
        terminal_authorization_3 = mock.MagicMock(
            terminal_no='3',
            access_token='header.payload.terminal_3',
            access_token_expires_at=to_utc_timestamp(
                datetime(2025, 7, 31, 12, 0, 0))
        )
        terminal_authorization_4 = mock.MagicMock(
            terminal_no='4',
            access_token='header.payload.terminal_4',
            access_token_expires_at=to_utc_timestamp(
                datetime(2025, 7, 31, 12, 0, 0))
        )
        for terminal_authorization in [
            terminal_authorization_1, terminal_authorization_2,
            terminal_authorization_3, terminal_authorization_4
        ]:
            key = terminal_authorization.access_token
            self.terminal_authorizations[key] = terminal_authorization

    def issue_transaction_number(self):
        '''取引番号を発行する。

            uuid.uuid4()を使用して取引番号を発行する。
            ※取引番号の発行方法は、フェーズ2以降に確定される。
            ※モデル定義後の設定次第では、不要になる可能性あり。

        Args:
            なし

        Returns:
            str型: 取引番号

        '''
        # 取引番号の発行
        # モデル定義後は別形式に変更される可能性あり
        transaction_number = str(uuid4())
        return transaction_number

    def get_terminal_authorization_by_access_token(
            self, terminal_access_token):
        '''店舗端末認証情報を取得する.

            認証トークンに一致するカードを取得する

        Args:
            terminal_access_token (str型): 認証トークン

        Returns:
            店舗端末認証情報: 指定された認証トークンに一致するモックオブジェクトがなければ、例外を発生させる.

        Raises:
            Exception: リクエストされた認証トークンで一致する店舗端末認証情報がない

        '''
        key = terminal_access_token
        try:
            terminal_authorization = self.terminal_authorizations[key]
        # トークン認証エラー
        # 質問シートにて認証トークンを使用して店舗端末認証情報を取得するとの回答あり。
        except KeyError:
            raise Exception('リクエストされた認証トークンを持つ店舗端末認証情報がない')
        return terminal_authorization

    def create_transaction(self, transaction_number):
        '''
            取引履歴情報を作成する。

        Args:
            transaction_number(str型)
            ※フェーズ1ではtransaction_numberでのレコードを作成する。
            ※フェーズ2以降では変更の可能性あり。

        Returns:
            None
            ※ フェーズ2以降では変更の可能性あり。

        '''

        self.transactions[transaction_number] = mock.MagicMock(
            transaction_number=transaction_number)
