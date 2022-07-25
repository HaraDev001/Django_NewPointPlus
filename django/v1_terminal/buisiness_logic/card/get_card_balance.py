from rest_framework import status
from utils.datetime_utility import now, to_utc_timestamp
from v1_terminal.data.ICardBalanceRepository import ICardBalanceRepository
from v1_terminal.data.ICardDetailRepository import ICardDetailRepository

from ..DTO.get_card_balance_instance import GetCardBalanceInstance


class GetCardBalance:
    '''
        GetCardBalanceクラス

        Attributes:
            card_detail_repository(ICardDetailRepository型):
            ICardDetailRepositoryを継承したオブジェクト
            card_balance_repository(ICardBalanceRepository型):
            ICardBalanceRepositoryを継承したオブジェクト

    '''

    def __init__(
        self, card_detail_repository: ICardDetailRepository,
        card_balance_repository: ICardBalanceRepository

    ):
        self.card_detail_repository: ICardDetailRepository =\
            card_detail_repository
        self.card_balance_repository: ICardBalanceRepository =\
            card_balance_repository

    def execute(self, pk, card_no, card_pin, terminal_access_token):
        '''
        CardBalanceSerializerに渡すためのinstanceを発行する。

        1. カード番号を元に各モデルから必要な情報を取得し、項目チェックを実行する。
        2. カード番号を元にカード残高情報を取得、集計する。
        3. CardBalanceSerializerに渡すためのinstanceを返す。

        Args:
            pk(str): URIから取得したカード番号
            card_no(str): カード番号
            card_pin(str): カードpin
            terminal_access_token(str): 認証トークン

        Returns:
            GetCardBalanceInstance型
            int型: HTTPステータスコード
        '''

        if pk != card_no:
            # URIのカード番号とreuqest内のカード番号の不一致
            return None, status.HTTP_400_BAD_REQUEST

        try:
            card = self.card_detail_repository.\
                identify_card(card_no, card_pin)

        except Exception:
            # 存在しないカード
            # カード番号に一致するカードがない
            return None, status.HTTP_200_OK

        try:
            terminal_authorization = self.card_detail_repository.\
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

        # service_user_policy=False, サービス利用許可なし
        if not card.service_user_policy:
            return None, status.HTTP_400_BAD_REQUEST

        # provider_id='', 事業者が結びついていないカード
        if card.provider_id == '':
            return None, status.HTTP_400_BAD_REQUEST

        # カード残高情報取得
        # balance_type毎に取得する。
        # balance_type = (暫定)0: 前払いバリュー, 1: 決済併用ボーナス, 2: 商品交換ボーナス
        prepaid_value_balance =\
            self.card_balance_repository.get_card_balance_by_type(card_no, 0)
        payable_bonus_balance =\
            self.card_balance_repository.get_card_balance_by_type(card_no, 1)
        product_exchange_bonus_balance =\
            self.card_balance_repository.get_card_balance_by_type(card_no, 2)

        return GetCardBalanceInstance(
            total_balance=prepaid_value_balance.total_balance +
            payable_bonus_balance.total_balance +
            product_exchange_bonus_balance.total_balance,
            prepaid_value=prepaid_value_balance,
            payable_bonus=payable_bonus_balance,
            product_exchange_bonus=product_exchange_bonus_balance
        ), status.HTTP_200_OK
