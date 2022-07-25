from rest_framework import status
from utils.datetime_utility import now, to_utc_timestamp
from v1_terminal.data.ITransactionGetRepository import \
    ITransactionGetRepository

from ..DTO.transaction_get_response import TransactionDetailResponse


class GetTransactionDetail:
    '''
        GetTransactionDetailクラス

        Attributes:
            transaction_repository(ITransactionGetRepository型):
            ITransactionGetRepositoryを継承したオブジェクト

    '''

    def __init__(self, transaction_repository: ITransactionGetRepository):
        self.transaction_repository: ITransactionGetRepository = transaction_repository

    def execute(self, terminal_access_token, transaction_number, pk):
        '''取引履歴詳細を取得する
            取引履歴詳細情報を取得する。
            1. requestから渡された認証トークンと取引番号を元に、データを取得する。
            2. 項目チェックを実行する。
            3. Serializerに渡すためのinstanceと、ステータスコードを返す。

        Args:
            terminal_access_token (str): 認証トークン
            transaction_number (str): リクエストから取得した取引番号
            pk (str): URIから取得した取引番号

        Returns:
            TransactionDetailResponse型
            int型: HTTPステータスコード

        '''
        # リクエスト内の取引番号とURIの取引番号の不一致
        if pk != transaction_number:
            return None, status.HTTP_400_BAD_REQUEST

        try:
            terminal_authorization = self.transaction_repository.\
                get_terminal_authorization(terminal_access_token)
        except Exception:
            # トークン認証エラー
            # リクエストされたトークンを保持する店舗端末認証情報がない
            return None, status.HTTP_401_UNAUTHORIZED

        # トークン有効期限切れ
        current_unixtime = int(to_utc_timestamp(now()))
        if current_unixtime > terminal_authorization.access_token_expires_at:
            return None, status.HTTP_401_UNAUTHORIZED

        try:
            transaction = self.transaction_repository.\
                get_transaction(transaction_number)
        except Exception:
            # 存在しない取引
            return None, status.HTTP_404_NOT_FOUND

        # 取引詳細内のカード情報を取得してカードの存在チェックを実行する。
        # モデル定義後に処理を変更する可能性あり。
        transaction_card_list = transaction.card

        for card in transaction_card_list:
            try:
                card = self.transaction_repository.get_card(card.card_no)
            except Exception:
                # カード番号に一致するカードがない
                return None, status.HTTP_404_NOT_FOUND
            # サービス利用許可なし
            if not card.service_user_policy:
                return None, status.HTTP_403_FORBIDDEN

        transaction_detail_response =\
            TransactionDetailResponse(
                transaction_type=transaction.transaction_type,
                transaction_at=transaction.transaction_at,
                transaction_number=transaction.transaction_number,
                transaction_status=transaction.transaction_status,
                company=transaction.company,
                shop=transaction.shop,
                terminal=transaction.terminal,
                transaction=transaction.transaction,
                card=transaction.card,
                card_merge=transaction.card_merge
            )
        return transaction_detail_response, status.HTTP_200_OK
