from rest_framework import status
from utils.datetime_utility import now, to_utc_timestamp
from v1_terminal.data.ICardActivateRepository import ICardActivateRepository


class ActivateCard:
    '''
        ActivateCardクラス

        Attributes:
            card_activate-repository(ICardActivateRepository型):
            ICardActivateRepositoryを継承したオブジェクト
    '''

    def __init__(
        self, card_activate_repository: ICardActivateRepository,
    ):
        self.card_activate_repository: ICardActivateRepository =\
            card_activate_repository

    def execute(self, pk, card_no, card_pin, terminal_access_token):
        '''
            カードをアクティベートする。
            1. URIから渡されたcard_noとrequest内で渡されたcard_noに齟齬がないかチェックする。
            2. カード番号、カードpinを元にカード情報を取得する。
            3. 認証トークンから店舗端末認証情報を取得する。
            4. 項目チェックを実行する。
            5. カードをアクティベートする。
            （暫定）card.stateを0（未アクティベート）から1（アクティベート済み）に変更する。

            Args:
                pk(str): URIから取得したカード番号
                card_no(str): カード番号
                card_pin(str): カードpin
                terminal_access_token(str): 認証トークン

            Returns:
                int型: HTTPステータスコード
        '''

        if pk != card_no:
            # URIのカード番号とreuqest内のカード番号の不一致
            return status.HTTP_400_BAD_REQUEST

        try:
            card = self.card_activate_repository.\
                identify_card(card_no, card_pin)
        except Exception:
            # 存在しないカード
            return status.HTTP_200_OK

        try:
            terminal_authorization = self.card_activate_repository.\
                get_terminal_authorization_by_access_token(
                    terminal_access_token)
        except Exception:
            # トークン認証エラー
            # リクエストされたトークンを保持する店舗端末認証情報がない
            return status.HTTP_200_OK

        # service_user_policy=False, サービス利用許可なし
        if not card.service_user_policy:
            return status.HTTP_400_BAD_REQUEST

        # 未アクティベートでないカード
        # 未アクティべート card.state == 0 は仮の状態。
        # モデルが定義された後に書き換える可能性あり
        if card.state != 0:
            return status.HTTP_400_BAD_REQUEST

        # トークン有効期限切れ
        current_unixtime = int(to_utc_timestamp(now()))
        if current_unixtime > terminal_authorization.access_token_expires_at:
            return status.HTTP_400_BAD_REQUEST

        # カードアクティベート処理
        # card.state = 1（アクティベート済みは暫定）
        card.state = 1
        # カード情報の保存
        self.card_activate_repository.save_card(card)
        return status.HTTP_200_OK
