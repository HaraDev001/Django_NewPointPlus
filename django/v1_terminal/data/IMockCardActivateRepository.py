from datetime import datetime
from unittest import mock

from utils.datetime_utility import to_utc_timestamp


class IMockCardActivateRepository():
    '''
    ICardActivateRepositoryを実装したクラス

        ICardDetailRepositoryを実装したモックオブジェクトを扱うクラス

        Attributes:
            cards (dict): カード情報を保持
            terminal_authorizations (dict): 店舗端末認証情報を保持
    '''

    def __init__(self):

        self.cards = dict()
        self.terminal_authorizations = dict()

        # カード情報
        card_101 = mock.MagicMock(
            card_no='9999999999990101', card_pin='0101', state=0,
            payment=True, service_user_policy=True,
            provider_id='110000001', company_user_policy=True)
        card_102 = mock.MagicMock(
            card_no='9999999999990102', card_pin='0102', state=0,
            payment=True, service_user_policy=False,
            provider_id='110000001', company_user_policy=True)
        card_103 = mock.MagicMock(
            card_no='9999999999990103', card_pin='0103', state=1,
            payment=True, service_user_policy=True,
            provider_id='110000001', company_user_policy=False)
        card_104 = mock.MagicMock(
            card_no='9999999999990104', card_pin='0104', state=3,
            payment=True, service_user_policy=True,
            provider_id='', company_user_policy=False)
        card_105 = mock.MagicMock(
            card_no='9999999999990105', card_pin='0105', state=0,
            payment=False, service_user_policy=False,
            provider_id='110000001', company_user_policy=True)
        card_106 = mock.MagicMock(
            card_no='9999999999990106', card_pin='0106', state=0,
            payment=False, service_user_policy=False,
            provider_id='110000001', company_user_policy=True)
        card_107 = mock.MagicMock(
            card_no='9999999999990107', card_pin='0107', state=0,
            payment=False, service_user_policy=True,
            provider_id='110000001', company_user_policy=False)
        card_108 = mock.MagicMock(
            card_no='9999999999990108', card_pin='0108', state=0,
            payment=False,
            service_user_policy=False,
            provider_id='110000001', company_user_policy=False)

        for card in [
                card_101, card_102, card_103, card_104,
                card_105, card_106, card_107, card_108,
                ]:
            key = card.card_no
            self.cards[key] = card

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

    def identify_card(self, card_no, card_pin):
        '''カード情報を取得する.

            カード番号およびPIN番号に一致するカードを取得する

        Args:
            card_no (str型): カード番号.

        Returns:
            カード情報: 指定されたカード番号およびPIN番号に一致するモックオブジェクトがなければ、例外を発生させる.

        Raises:
            Exception: リクエストされたカード番号で一致するカードがない
            Exception: リクエストされたカード番号＆PINで一致するカードがない

        '''
        key = card_no
        try:
            card = self.cards[key]
            if card.card_pin == card_pin:
                return self.cards[key]
            else:
                raise Exception('リクエストされたカード番号＆PINで一致するカードがない')
        except KeyError:
            raise Exception('リクエストされたカード番号で一致するカードがない')

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

    def save_card(self, card):
        '''カード情報を保存する.

            カード情報を保存する。

        Args:
            card_no (MagicMock型): カード情報を保存したモックオブジェクト.

        Returns:
            なし

        '''
        key = card.card_no
        self.cards[key] = card
