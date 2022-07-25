from v1_card.data.IAccessTokenRepository \
    import IAccessTokenRepository

from unittest import mock


class IMockAccessTokenRepository(
    IAccessTokenRepository
):
    def __init__(self):

        # カード情報
        self.cards = dict()
        card_101 = mock.MagicMock(
            card_no='9999999999990101', card_pin='0101', state=1,
            payment=True, service_user_policy=True, company_user_policy=True,
            provider_id='0000000001')
        card_102 = mock.MagicMock(
            card_no='9999999999990102', card_pin='0102', state=1,
            payment=True, service_user_policy=False, company_user_policy=True,
            provider_id='0000000001')
        card_103 = mock.MagicMock(
            card_no='9999999999990103', card_pin='0103', state=1,
            payment=True, service_user_policy=True, company_user_policy=False,
            provider_id='0000000001')
        card_104 = mock.MagicMock(
            card_no='9999999999990104', card_pin='0104', state=1,
            payment=True, service_user_policy=False, company_user_policy=False,
            provider_id='0000000001')
        card_105 = mock.MagicMock(
            card_no='9999999999990105', card_pin='0105', state=1,
            payment=False, service_user_policy=True, company_user_policy=True,
            provider_id='0000000001')
        card_106 = mock.MagicMock(
            card_no='9999999999990106', card_pin='0106', state=1,
            payment=False, service_user_policy=False, company_user_policy=True,
            provider_id='0000000001')
        card_107 = mock.MagicMock(
            card_no='9999999999990107', card_pin='0107', state=1,
            payment=False, service_user_policy=True, company_user_policy=False,
            provider_id='0000000001')
        card_108 = mock.MagicMock(
            card_no='9999999999990108', card_pin='0108', state=1,
            payment=False,
            service_user_policy=False,
            company_user_policy=False,
            provider_id='0000000001')

        card_201 = mock.MagicMock(
            card_no='9999999999990201', card_pin='0201', state=2,
            payment=True, service_user_policy=True, company_user_policy=True,
            provider_id='0000000001')
        card_202 = mock.MagicMock(
            card_no='9999999999990202', card_pin='0202', state=2,
            payment=True, service_user_policy=False, company_user_policy=True,
            provider_id='0000000001')
        card_203 = mock.MagicMock(
            card_no='9999999999990203', card_pin='0203', state=2,
            payment=True, service_user_policy=True, company_user_policy=False,
            provider_id='0000000001')
        card_204 = mock.MagicMock(
            card_no='9999999999990204', card_pin='0204', state=2,
            payment=True, service_user_policy=False, company_user_policy=False,
            provider_id='0000000001')

        card_205 = mock.MagicMock(
            card_no='9999999999990205', card_pin='0205', state=2,
            payment=False, service_user_policy=True, company_user_policy=True,
            provider_id='0000000001')

        card_206 = mock.MagicMock(
            card_no='9999999999990206', card_pin='0206', state=2,
            payment=False, service_user_policy=False, company_user_policy=True,
            provider_id='0000000001')

        card_207 = mock.MagicMock(
            card_no='9999999999990207', card_pin='0207', state=2,
            payment=False, service_user_policy=True, company_user_policy=False,
            provider_id='0000000001')

        card_208 = mock.MagicMock(
            card_no='9999999999990208', card_pin='0208', state=2,
            payment=False,
            service_user_policy=False,
            company_user_policy=False,
            provider_id='0000000001')

        for card in [
                card_101, card_102, card_103, card_104,
                card_105, card_106, card_107, card_108,
                card_201, card_202, card_203, card_204,
                card_205, card_206, card_207, card_208
                ]:
            key = card.card_no
            self.cards[key] = card

        # カードアクセス認証情報
        self.card_access_authorization = dict()

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

    def get_card(self, card_no):
        '''カード情報を取得する.

            カード情報を取得する.

        Args:
            card_no (str型): カード番号.

        Returns:
            カード情報: 指定されたカード番号のモックオブジェクトがなければ、例外を発生させる.

        Raises:
            Exception: リクエストされたカード番号で一致するカードがない

        '''

        key = card_no
        try:
            card = self.cards[key]
            return card
        except KeyError:
            raise Exception('リクエストされたカード番号で一致するカードがない')
        except Exception as e:
            raise e

    def get_card_access_authorization(self, card_no):
        '''カードアクセス認証情報を取得する.

            カードアクセス認証情報を取得する.

        Args:
            card_no (str型): カード番号.

        Returns:
            カードアクセス情報: 指定されたカード番号のモックオブジェクトがなければ、例外を発生させる.

        Raises:
            Exception: リクエストされたカード番号で一致するカードアクセス情報がない

        '''
        try:
            return self.card_access_authorization[card_no]
        except KeyError:
            raise Exception('リクエストされたカード番号で一致するカードアクセス情報がない')
        except Exception as e:
            raise e

    def get_or_create_card_access_authorization(self, card_no):
        '''カードアクセス認証情報を取得する.

            カードアクセス認証情報を取得する.

        Args:
            card_no (str型): カード番号.

        Returns:
            カードアクセス情報: 指定されたカード番号のモックオブジェクトがなければ、新しいモックオブジェクトを生成する.

        '''
        try:
            return self.card_access_authorization[card_no]
        except KeyError:
            return mock.MagicMock()

    def save_card_access_authorization(self, card_access_auth):
        '''カードアクセス認証情報を保存する.

            カードアクセス認証情報を保存する.

        Args:
            card_access_auth (MagicMock型): モックオブジェクト.

        Returns:
            なし

        '''
        card_no = card_access_auth.card_no
        self.card_access_authorization[card_no] = card_access_auth
