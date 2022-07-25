from unittest import mock
from rest_framework import status
from django.test import SimpleTestCase
from v1_card.data.IAccessTokenRepository import IAccessTokenRepository
from v1_card.data.IMockAccessTokenRepository import IMockAccessTokenRepository
from v1_card.buisiness_logic.access_token.issue_access_token \
    import IssueAccessToken
from v1_card.buisiness_logic.access_token.common \
    import decode_token_to_json
from utils.datetime_utility import (now,
                                    to_utc_timestamp,
                                    get_datetime_hours_later_from
                                    )


class AccessTokenIssueTests(SimpleTestCase):

    # カード情報[あり] アクティベート [済み] 決済 [可能] サービス利用許可 [あり] 事業者利用規約 [同意]
    def test_send_card_101_success(self):

        test_repository: IAccessTokenRepository = IMockAccessTokenRepository()
        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute('9999999999990101', '0101')

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNotNone(access_token_response)

        access_token_payload_json = decode_token_to_json(
            access_token_response.access_token)

        self.assertEqual(
            access_token_payload_json['card_no'], '9999999999990101'
            )

        utc_timestamp_current = to_utc_timestamp(
            now()
        )

        utc_timestamp_1_hour_later = to_utc_timestamp(
            get_datetime_hours_later_from(now(), hours=1)
        )

        # アクセストークンの有効期限
        self.assertLessEqual(
            utc_timestamp_current,
            access_token_response.access_token_expire_at
            )

        self.assertLessEqual(
            access_token_response.access_token_expire_at,
            utc_timestamp_1_hour_later
            )

        refresh_token_payload_json = decode_token_to_json(
            access_token_response.refresh_token)

        self.assertEqual(
            refresh_token_payload_json['card_no'], '9999999999990101'
            )

    # カード情報[あり] アクティベート [済み] 決済 [可能] サービス利用許可 [なし] 事業者利用規約 [同意]
    def test_send_card_102_fail(self):

        test_repository: IAccessTokenRepository = IMockAccessTokenRepository()
        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute('9999999999990102', '0102')

        self.assertEqual(status_code, status.HTTP_403_FORBIDDEN)
        # アクセストークンの発行はない
        self.assertIsNone(access_token_response)

        card_auth = test_repository.get_or_create_card_access_authorization('9999999999990102')
        # MagicMockの仕様上、定義されていない属性を取得しようとすると、
        # その属性に新しいモックを割り当てる。
        # カードアクセス認証情報がないことを、stateにモックオブジェクトが
        # 割り当てられていることでシュミレートする
        self.assertIsInstance(card_auth.state, mock.MagicMock)

    # カード情報[あり] アクティベート [済み] 決済 [可能] サービス利用許可 [あり] 事業者利用規約 [未同意]
    def test_send_card_103_fail(self):

        test_repository: IAccessTokenRepository = IMockAccessTokenRepository()
        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute('9999999999990103', '0103')

        self.assertEqual(status_code, status.HTTP_403_FORBIDDEN)
        # アクセストークンの発行はない
        self.assertIsNone(access_token_response)

        card_auth = test_repository.get_or_create_card_access_authorization('9999999999990103')
        # MagicMockの仕様上、定義されていない属性を取得しようとすると、
        # その属性に新しいモックを割り当てる。
        # カードアクセス認証情報がないことを、stateにモックオブジェクトが
        # 割り当てられていることでシュミレートする
        self.assertIsInstance(card_auth.state, mock.MagicMock)

    # カード情報[あり] アクティベート [済み] 決済 [可能] サービス利用許可 [なし]] 事業者利用規約 [未同意]
    def test_send_card_104_fail(self):

        test_repository: IAccessTokenRepository = IMockAccessTokenRepository()
        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute('9999999999990104', '0104')

        self.assertEqual(status_code, status.HTTP_403_FORBIDDEN)
        # アクセストークンの発行はない
        self.assertIsNone(access_token_response)

        card_auth = test_repository.get_or_create_card_access_authorization('9999999999990104')
        # MagicMockの仕様上、定義されていない属性を取得しようとすると、
        # その属性に新しいモックを割り当てる。
        # カードアクセス認証情報がないことを、stateにモックオブジェクトが
        # 割り当てられていることでシュミレートする
        self.assertIsInstance(card_auth.state, mock.MagicMock)

    # カード情報[あり] アクティベート [済み] 決済 [不能] サービス利用許可 [あり] 事業者利用規約 [同意]
    def test_send_card_105_fail(self):

        test_repository: IAccessTokenRepository = IMockAccessTokenRepository()
        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute('9999999999990105', '0105')

        self.assertEqual(status_code, status.HTTP_403_FORBIDDEN)
        # アクセストークンの発行はない
        self.assertIsNone(access_token_response)

        card_auth = test_repository.get_or_create_card_access_authorization('9999999999990105')
        # MagicMockの仕様上、定義されていない属性を取得しようとすると、
        # その属性に新しいモックを割り当てる。
        # カードアクセス認証情報がないことを、stateにモックオブジェクトが
        # 割り当てられていることでシュミレートする
        self.assertIsInstance(card_auth.state, mock.MagicMock)

    # カード情報[あり] アクティベート [済み] 決済 [不能] サービス利用許可 [なし] 事業者利用規約 [同意]
    def test_send_card_106_fail(self):

        test_repository: IAccessTokenRepository = IMockAccessTokenRepository()
        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute('9999999999990106', '0106')

        self.assertEqual(status_code, status.HTTP_403_FORBIDDEN)
        # アクセストークンの発行はない
        self.assertIsNone(access_token_response)

        card_auth = test_repository.get_or_create_card_access_authorization('9999999999990106')
        # MagicMockの仕様上、定義されていない属性を取得しようとすると、
        # その属性に新しいモックを割り当てる。
        # カードアクセス認証情報がないことを、stateにモックオブジェクトが
        # 割り当てられていることでシュミレートする
        self.assertIsInstance(card_auth.state, mock.MagicMock)

    # カード情報[あり] アクティベート [済み] 決済 [不能] サービス利用許可 [あり] 事業者利用規約 [未同意]

    def test_send_card_107_fail(self):

        test_repository: IAccessTokenRepository = IMockAccessTokenRepository()
        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute('9999999999990107', '0107')

        self.assertEqual(status_code, status.HTTP_403_FORBIDDEN)
        # アクセストークンの発行はない
        self.assertIsNone(access_token_response)

        card_auth = test_repository.get_or_create_card_access_authorization('9999999999990107')
        # MagicMockの仕様上、定義されていない属性を取得しようとすると、
        # その属性に新しいモックを割り当てる。
        # カードアクセス認証情報がないことを、stateにモックオブジェクトが
        # 割り当てられていることでシュミレートする
        self.assertIsInstance(card_auth.state, mock.MagicMock)

    # カード情報[あり] アクティベート [済み] 決済 [不能] サービス利用許可 [なし] 事業者利用規約 [未同意]
    def test_send_card_108_fail(self):

        test_repository: IAccessTokenRepository = IMockAccessTokenRepository()
        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute('9999999999990108', '0108')

        self.assertEqual(status_code, status.HTTP_403_FORBIDDEN)
        # アクセストークンの発行はない
        self.assertIsNone(access_token_response)

        card_auth = test_repository.get_or_create_card_access_authorization('9999999999990108')
        # MagicMockの仕様上、定義されていない属性を取得しようとすると、
        # その属性に新しいモックを割り当てる。
        # カードアクセス認証情報がないことを、stateにモックオブジェクトが
        # 割り当てられていることでシュミレートする
        self.assertIsInstance(card_auth.state, mock.MagicMock)

    # # ----------------------------------------------------------------------

    # カード情報[あり] アクティベート [なし] 決済 [可能] サービス利用許可 [あり] 事業者利用規約 [同意]
    def test_send_card_201_fail(self):

        test_repository: IAccessTokenRepository = IMockAccessTokenRepository()
        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute('9999999999990201', '0201')

        self.assertEqual(status_code, status.HTTP_200_OK)
        # アクセストークンの発行はない
        self.assertIsNone(access_token_response)

        card_auth = test_repository.get_card_access_authorization('9999999999990201')

        self.assertIs(type(card_auth.state), int)
        # カードアクセス認証情報は存在し、未発行となっている
        self.assertEqual(card_auth.state, 0)

    # カード情報[あり] アクティベート [なし] 決済 [可能] サービス利用許可 [なし] 事業者利用規約 [同意]
    def test_send_card_202_fail(self):

        test_repository: IAccessTokenRepository = IMockAccessTokenRepository()
        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute('9999999999990202', '0202')

        self.assertEqual(status_code, status.HTTP_403_FORBIDDEN)
        # アクセストークンの発行はない
        self.assertIsNone(access_token_response)

        card_auth = test_repository.get_or_create_card_access_authorization('9999999999990202')

        # MagicMockの仕様上、定義されていない属性を取得しようとすると、
        # その属性に新しいモックを割り当てる。
        # カードアクセス認証情報がないことを、stateにモックオブジェクトが
        # 割り当てられていることでシュミレートする
        self.assertIsInstance(card_auth.state, mock.MagicMock)

    # カード情報[あり] アクティベート [なし] 決済 [可能] サービス利用許可 [あり] 事業者利用規約 [未同意]
    def test_send_card_203_fail(self):

        test_repository: IAccessTokenRepository = IMockAccessTokenRepository()
        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute('9999999999990203', '0203')

        self.assertEqual(status_code, status.HTTP_403_FORBIDDEN)
        # アクセストークンの発行はない
        self.assertIsNone(access_token_response)

        card_auth = test_repository.get_or_create_card_access_authorization('9999999999990203')
        # MagicMockの仕様上、定義されていない属性を取得しようとすると、
        # その属性に新しいモックを割り当てる。
        # カードアクセス認証情報がないことを、stateにモックオブジェクトが
        # 割り当てられていることでシュミレートする
        self.assertIsInstance(card_auth.state, mock.MagicMock)

    # カード情報[あり] アクティベート [なし] 決済 [可能] サービス利用許可 [なし]] 事業者利用規約 [未同意]
    def test_send_card_204_fail(self):

        test_repository: IAccessTokenRepository = IMockAccessTokenRepository()
        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute('9999999999990204', '0204')

        self.assertEqual(status_code, status.HTTP_403_FORBIDDEN)
        # アクセストークンの発行はない
        self.assertIsNone(access_token_response)

        card_auth = test_repository.get_or_create_card_access_authorization('9999999999990204')
        # MagicMockの仕様上、定義されていない属性を取得しようとすると、
        # その属性に新しいモックを割り当てる。
        # カードアクセス認証情報がないことを、stateにモックオブジェクトが
        # 割り当てられていることでシュミレートする
        self.assertIsInstance(card_auth.state, mock.MagicMock)

    # カード情報[あり] アクティベート [なし] 決済 [不能] サービス利用許可 [あり] 事業者利用規約 [同意]
    def test_send_card_205_fail(self):

        test_repository: IAccessTokenRepository = IMockAccessTokenRepository()
        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute('9999999999990205', '0205')

        self.assertEqual(status_code, status.HTTP_403_FORBIDDEN)
        # アクセストークンの発行はない
        self.assertIsNone(access_token_response)

        card_auth = test_repository.get_or_create_card_access_authorization('9999999999990205')
        # MagicMockの仕様上、定義されていない属性を取得しようとすると、
        # その属性に新しいモックを割り当てる。
        # カードアクセス認証情報がないことを、stateにモックオブジェクトが
        # 割り当てられていることでシュミレートする
        self.assertIsInstance(card_auth.state, mock.MagicMock)

    # カード情報[あり] アクティベート [なし] 決済 [不能] サービス利用許可 [なし] 事業者利用規約 [同意]
    def test_send_card_206_fail(self):

        test_repository: IAccessTokenRepository = IMockAccessTokenRepository()
        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute('9999999999990206', '0206')

        self.assertEqual(status_code, status.HTTP_403_FORBIDDEN)
        # アクセストークンの発行はない
        self.assertIsNone(access_token_response)

        card_auth = test_repository.get_or_create_card_access_authorization('9999999999990206')
        # MagicMockの仕様上、定義されていない属性を取得しようとすると、
        # その属性に新しいモックを割り当てる。
        # カードアクセス認証情報がないことを、stateにモックオブジェクトが
        # 割り当てられていることでシュミレートする
        self.assertIsInstance(card_auth.state, mock.MagicMock)

    # カード情報[あり] アクティベート [なし] 決済 [不能] サービス利用許可 [あり] 事業者利用規約 [未同意]
    def test_send_card_207_fail(self):

        test_repository: IAccessTokenRepository = IMockAccessTokenRepository()
        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute('9999999999990207', '0207')

        self.assertEqual(status_code, status.HTTP_403_FORBIDDEN)
        # アクセストークンの発行はない
        self.assertIsNone(access_token_response)

        card_auth = test_repository.get_or_create_card_access_authorization('9999999999990207')
        # MagicMockの仕様上、定義されていない属性を取得しようとすると、
        # その属性に新しいモックを割り当てる。
        # カードアクセス認証情報がないことを、stateにモックオブジェクトが
        # 割り当てられていることでシュミレートする
        self.assertIsInstance(card_auth.state, mock.MagicMock)

    # カード情報[あり] アクティベート [なし] 決済 [不能] サービス利用許可 [なし] 事業者利用規約 [未同意]
    def test_send_card_208_fail(self):

        test_repository: IAccessTokenRepository = IMockAccessTokenRepository()
        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute('9999999999990208', '0208')

        self.assertEqual(status_code, status.HTTP_403_FORBIDDEN)
        # アクセストークンの発行はない
        self.assertIsNone(access_token_response)

        card_auth = test_repository.get_or_create_card_access_authorization('9999999999990208')
        # MagicMockの仕様上、定義されていない属性を取得しようとすると、
        # その属性に新しいモックを割り当てる。
        # カードアクセス認証情報がないことを、stateにモックオブジェクトが
        # 割り当てられていることでシュミレートする
        self.assertIsInstance(card_auth.state, mock.MagicMock)

    def test_send_wrong_card_fail(self):
        test_repository: IAccessTokenRepository = IMockAccessTokenRepository()
        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute('9999999999990XXX', '0101')

        # このようなカードはない

        self.assertEqual(status_code, status.HTTP_400_BAD_REQUEST)
        # アクセストークンの発行はない
        self.assertIsNone(access_token_response)

        # PIN番号が違う

        access_token_response, status_code = \
            issue_access_token.execute('9999999999990101', 'XXXX')

        self.assertEqual(status_code, status.HTTP_400_BAD_REQUEST)
        # アクセストークンの発行はない
        self.assertIsNone(access_token_response)

    def test_send_wrong_card_pin_fail(self):
        test_repository: IAccessTokenRepository = IMockAccessTokenRepository()
        issue_access_token = IssueAccessToken(test_repository)

        # PIN番号が違う

        access_token_response, status_code = \
            issue_access_token.execute('9999999999990101', 'XXXX')

        self.assertEqual(status_code, status.HTTP_400_BAD_REQUEST)
        # アクセストークンの発行はない
        self.assertIsNone(access_token_response)
