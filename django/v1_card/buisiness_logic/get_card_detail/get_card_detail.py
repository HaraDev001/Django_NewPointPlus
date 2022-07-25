from rest_framework import status
from utils.datetime_utility import today
from v1_card.data.ICardDetailRepository import ICardDetailRepository

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

    def execute(self, card_no, access_token_data):
        '''
        CardDetailSerializerに渡すためのinstanceを発行する。

        1. カード番号を元に各モデルから必要な情報を取得し、項目チェックを実行する。
        2. CardDetailSerializerに渡すためのinsrtanceを返す。

        Args:
            card_no(str): カード番号

        Returns:
            GetCardDetailInstance型
            int型: HTTPステータスコード
        '''

        try:
            card = self.card_detail_repository.\
                get_card_by_no(card_no)
            card_config = self.card_detail_repository.\
                get_card_config_by_no(card_no)
            card_transaction = self.card_detail_repository.\
                get_card_transaction_by_no(card_no)
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

        return GetCardDetailInstance(
            card_config_name=card_config.card_config_name,
            card_design=card_config.card_design,
            card_no=card.card_no,
            card_status=card.state,
            currency_unit=card_config,
            transaction_limit_value=card_config,
            transaction_result_value=card_transaction
        ), status.HTTP_200_OK
