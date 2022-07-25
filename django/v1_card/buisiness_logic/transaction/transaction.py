from v1_card.data.ITransactionRepository import ITransactionRepository
from v1_card.data.IAccessTokenRepository import IAccessTokenRepository
from datetime import date, datetime
from rest_framework import status
from utils.datetime_utility import now, to_utc_timestamp

from unittest import mock

class Transaction:

    def __init__(self, accesstoken_repository: IAccessTokenRepository, transaction_repository: ITransactionRepository):
        self.accesstoken_repository: IAccessTokenRepository = accesstoken_repository
        self.transaction_repository: ITransactionRepository = transaction_repository

    def execute(self, card_number, transaction_id, request_data):
        '''取引履歴詳細情報を取得する.
            取引履歴詳細情報を取得する.
        Args:
            card_number (str型): カード番号.
			transaction_id (str型): 取引番号.
            request_data : アクセストークン.
        Returns:
            取引履歴詳細情報: 指定されたカード番号、取引番号のモックオブジェクトがなければ、Noneを返却する.
            ステータス：レスポンスステータス
        '''
        try:
            card = self.accesstoken_repository.get_card(card_number)
            token_info = self.accesstoken_repository.get_card_access_authorization(card_number)
        except Exception:
            # カード番号に一致するカードがない
            return None, status.HTTP_200_OK
        if not request_data:
            return None, status.HTTP_400_BAD_REQUEST
        if (request_data != token_info.access_token):
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
            transaction = self.transaction_repository.get_transaction(card_number, transaction_id)
            return transaction, status.HTTP_200_OK