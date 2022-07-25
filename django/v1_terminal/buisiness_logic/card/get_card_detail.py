from rest_framework import status
from utils.datetime_utility import now, to_utc_timestamp
from v1_terminal.data.ICardDetailRepository import ICardDetailRepository

from ..DTO.get_card_detail_instance import GetCardDetailInstance


class GetCardDetail:
    '''
        GetCardDetailクラス

        Attributes:
            card_detail_repository(ICardDetailRepository型):
            ICardDetailRepositoryを継承したオブジェクト
    '''

    def __init__(
        self, card_detail_repository: ICardDetailRepository,
    ):
        self.card_detail_repository: ICardDetailRepository =\
            card_detail_repository

    def execute(self, pk, card_no, card_pin, terminal_access_token):
        '''
        CardDetailSerializerに渡すためのinstanceを発行する。

        1. カード番号を元に各モデルから必要な情報を取得し、項目チェックを実行する。
        2. CardDetailSerializerに渡すためのinstanceを返す。

        Args:
            pk(str): URIから取得したカード番号
            card_no(str): カード番号
            card_pin(str): カードpin
            terminal_access_token(str): 認証トークン

        Returns:
            GetCardDetailInstance型
            int型: HTTPステータスコード
        '''
        if pk != card_no:
            # URIのカード番号とreuqest内のカード番号の不一致
            return None, status.HTTP_400_BAD_REQUEST

        try:
            card = self.card_detail_repository.\
                identify_card(card_no, card_pin)
            card_config = self.card_detail_repository.\
                get_card_config_by_no(card_no)
            card_transaction = self.card_detail_repository.\
                get_card_transaction_by_no(card_no)

        except Exception:
            # 存在しないカード
            # カード番号&カードpinに一致するカードがない
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

        return GetCardDetailInstance(
            card_config_name=card_config.card_config_name,
            card_design=card_config.card_design,
            card_no=card.card_no,
            card_status=card.state,
            transaction_limit_value=card_config,
            transaction_result_value=card_transaction
        ), status.HTTP_200_OK
