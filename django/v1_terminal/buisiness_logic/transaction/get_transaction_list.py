from rest_framework import status
from utils.datetime_utility import now, to_utc_timestamp
from v1_terminal.data.ITransactionGetRepository import \
    ITransactionGetRepository

from ..DTO.transaction_get_response import TransactionListResponse


class GetTransactionList:

    def __init__(self, transaction_repository: ITransactionGetRepository):
        self.transaction_repository: ITransactionGetRepository = transaction_repository

    def execute(
        self, terminal_access_token, transaction_type, transaction_start, transaction_end, transaction_status,
        terminal_no, card_no, magnetic_information
    ):
        '''取引履歴一覧情報を取得する.
            取引履歴一覧情報を取得する.
        Args:
            terminal_access_token (str): 認証トークン
            transaction_type (int): リクエストから取得した取引種別
            transaction_start (DateTime): リクエストから取得した取引日時（From）
            transaction_end (DateTime): リクエストから取得した取引日時（To）
            transaction_status (int): リクエストから取得した取引ステータス
            terminal_no (str): リクエストから取得した端末番号
            card_no (str):  リクエストから取得したカード番号
            magnetic_information (str): リクエストから取得した磁気情報
        Returns:
            取引履歴一覧情報 (list): 指定された情報がなければ、空のリストを返却する。
            ステータス (int)：HTTPステータスコード
        '''
        if card_no:
            try:
                card = self.transaction_repository.get_card(card_no)
            except Exception:
                # カード番号に一致するカードがない
                return None, status.HTTP_200_OK
            # サービス利用許可なし
            if not card.service_user_policy:
                return None, status.HTTP_403_FORBIDDEN

        try:
            terminal_authorization = self.transaction_repository.\
                get_terminal_authorization(terminal_access_token)
        except Exception:
            # トークン認証エラー
            # リクエストされたトークンを保持する店舗端末認証情報がない
            return None, status.HTTP_401_UNAUTHORIZED

        # 取引日時の終了日時が開始日時よりも前の日時
        if transaction_start and transaction_end:
            if transaction_end < transaction_start:
                return None, status.HTTP_400_BAD_REQUEST

        # トークン有効期限切れ
        current_unixtime = int(to_utc_timestamp(now()))
        if current_unixtime > terminal_authorization.access_token_expires_at:
            return None, status.HTTP_401_UNAUTHORIZED

        authorization_terminal_no = terminal_authorization.terminal_no
        transaction_list = self.transaction_repository.get_transaction_list(
            authorization_terminal_no, transaction_type, transaction_start, transaction_end, transaction_status,
            terminal_no, card_no, magnetic_information
        )
        return transaction_list, status.HTTP_200_OK

    def execute_sort(self, transaction_list, start_index, item_number, sort_order):
        '''取引履歴一覧情報を指定の開始位置、取得件数、並び順でフィルターをかける.
            取引履歴一覧情報を指定の開始位置、取得件数、並び順でフィルターをかける.
        Args:
            transaction_list (list): 並び変え対象となるリスト
            start_index (int型): 開始位置.
            item_number (int型): 取得件数.
            sort_order (str型): 並び順. asc or desc
        Returns:
            TransactionListResponse型
        '''

        reverse = False if sort_order == 'asc' else True
        data_sorted = sorted(transaction_list, key=lambda x: x.transaction_at, reverse=reverse)

        index = 0
        count = item_number
        response_list = []
        for data in data_sorted:
            if index >= start_index and count > 0:
                response_list.append(data)
                count -= 1
            index += 1
        return TransactionListResponse(transaction_history=response_list)
