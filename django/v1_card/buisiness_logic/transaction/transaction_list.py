from v1_card.data.ITransactionRepository import ITransactionRepository
from v1_card.data.IAccessTokenRepository import IAccessTokenRepository
from datetime import date, datetime
from rest_framework import status
from utils.datetime_utility import now, to_utc_timestamp

from unittest import mock

class TransactionList:

    def __init__(self, accesstoken_repository: IAccessTokenRepository, transaction_repository: ITransactionRepository):
        self.accesstoken_repository: IAccessTokenRepository = accesstoken_repository
        self.transaction_repository: ITransactionRepository = transaction_repository

    def execute(self, card_number, access_token, search):
        '''取引履歴一覧情報を取得する.
            取引履歴一覧情報を取得する.
        Args:
            card_number (str型): カード番号.
            access_token : アクセストークン.
        Returns:
            取引履歴一覧情報: 指定されたカード番号、取引番号のモックオブジェクトがなければ、Noneを返却する.
            ステータス：レスポンスステータス
        '''
        try:
            card = self.accesstoken_repository.get_card(card_number)
            token_info = self.accesstoken_repository.get_card_access_authorization(card_number)
        except Exception:
            # カード番号に一致するカードがない
            return None, status.HTTP_200_OK
        if not access_token:
            return None, status.HTTP_400_BAD_REQUEST
        if (access_token != token_info.access_token):
            return None, status.HTTP_400_BAD_REQUEST
        #state == 1 でアクティベート済みは、仮の状態。
        if card.state == 2:
            return None, status.HTTP_200_OK
        # card_status=3, カードが破棄状態
        if card.state == 3:
            return None, status.HTTP_200_OK
        # provider_id='', 事業者が結びついていないカード
        if card.provider_id == '':
            return None, status.HTTP_200_OK
        # トークンステータスエラー
        if token_info.state == 2:
            return None, status.HTTP_400_BAD_REQUEST
        # サービス利用許可なし
        if not card.service_user_policy:
            return None, status.HTTP_400_BAD_REQUEST
        # トークン有効期限切れ
        current_unixtime = int(to_utc_timestamp(now()))
        if current_unixtime >= token_info.access_token_expire_at:
            return None, status.HTTP_400_BAD_REQUEST
        if card.state == 1:
            transaction_list = self.transaction_repository.get_transaction_list(card_number, search)
            return transaction_list, status.HTTP_200_OK


    def execute_sort(self, transaction_list, start_index, item_number, sort_order):
        '''取引履歴一覧情報を指定の開始位置、取得件数、並び順でフィルターをかける.
            取引履歴一覧情報を指定の開始位置、取得件数、並び順でフィルターをかける.
        Args:
            start_index (int型): 開始位置.
			item_number (int型): 取得件数.
			sort_order (str型): 並び順. asc or desc
        Returns:
            取引履歴一覧情報: 指定された開始位置、取得件数、並び順のモックオブジェクトがなければ、空のリストを返却する.
        '''

        reverse= True if sort_order == 'asc' else False
        start_index = 0 if not start_index else start_index
        item_number = len(transaction_list) if not item_number else item_number
        data_sorted = sorted(transaction_list, key=lambda x:x['transaction_at'], reverse=reverse)

        index = 0
        count = item_number
        response_list = []
        for data in data_sorted:
            if index >= start_index and count > 0:
                response_list.append(data)
            index = index + 1
            count = count - 1
        return  response_list