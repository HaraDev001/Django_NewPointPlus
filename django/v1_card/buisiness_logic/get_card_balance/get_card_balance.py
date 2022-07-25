from rest_framework import status
from utils.datetime_utility import today
from v1_card.data.ICardBalanceRepository import ICardBalanceRepository
from v1_card.data.ICardDetailRepository import ICardDetailRepository

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


    def execute(self, card_no, access_token_data):
        '''
        CardBalanceSerializerに渡すためのinstanceを発行する。

        1. カード番号を元に各モデルから必要な情報を取得し、項目チェックを実行する。
        2. カード番号を元にカード残高情報を取得、集計する。
        2. CardBalanceSerializerに渡すためのinsrtanceを返す。

        Args:
            card_no(str): カード番号
            access_token_data(str): アクセストークンデータ

        Returns:
            GetCardBalanceInstance型
            int型: HTTPステータスコード
        '''

        try:
            card = self.card_detail_repository.\
                get_card_by_no(card_no)
            card_access_authorization = self.card_detail_repository.\
                get_card_access_authorization_by_no(card_no)
        except Exception:
            # カード番号に一致するカードがない
            return None, status.HTTP_200_OK

        if card.state == 2:
            return None, status.HTTP_200_OK
        # card_status=3, カードが破棄状態
        if card.state == 3:
            return None, status.HTTP_200_OK
        # provider_id='', 事業者が結びついていないカード
        if card.provider_id == '':
            return None, status.HTTP_200_OK

        # 仮のトークン認証チェック部分
        # request.bodyのデータとアクセス認証情報のトークンデータを比較する。
        # モデル定義後書き換える可能性あり
        # トークン認証エラー
        if (access_token_data !=
                card_access_authorization.access_token):
            return None, status.HTTP_400_BAD_REQUEST
        # card_access_token_state = 2, トークンステータスエラー
        if card_access_authorization.access_token_state == 2:
            return None, status.HTTP_400_BAD_REQUEST
        # service_user_policy=False, サービス利用許可なし
        if not card.service_user_policy:
            return None, status.HTTP_400_BAD_REQUEST
        # expires_at < today(), トークン有効期限切れ
        if card_access_authorization.expires_at < today():
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
