from rest_framework import status
from django.test import SimpleTestCase
from v1_card.data.IAccessTokenRepository import IAccessTokenRepository
from v1_card.data.IMockAccessTokenRepository import IMockAccessTokenRepository
from v1_card.buisiness_logic.access_token.issue_access_token \
    import IssueAccessToken
from v1_card.buisiness_logic.access_token.invalidate_access_token \
    import InvalidateAccessToken

from v1_card.buisiness_logic.access_token.common import decode_token_to_json


class AccessTokenInvalidateTests(SimpleTestCase):
    # カード情報[あり] アクティベート [済み] 決済 [可能] サービス利用許可 [あり] 事業者利用規約 [同意]
    def test_send_card_101_success(self):
        # 予めアクセストークンを発行しておく
        test_repository: IAccessTokenRepository = IMockAccessTokenRepository()
        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute('9999999999990101', '0101')

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNotNone(access_token_response)

        access_token_payload_json = decode_token_to_json(
            access_token_response.access_token)
        refresh_token_payload_json = decode_token_to_json(
            access_token_response.refresh_token)

        self.assertEqual(
            access_token_payload_json['card_no'], '9999999999990101'
            )
        self.assertEqual(
            refresh_token_payload_json['card_no'], '9999999999990101'
            )

        card_access_auth = test_repository.get_card_access_authorization('9999999999990101')
        # 有効となっているか
        self.assertEqual(card_access_auth.state, 1)

        # 失効
        invalidate_access_token = InvalidateAccessToken(test_repository)
        status_code = invalidate_access_token.execute(
                access_token_response.access_token,
                access_token_response.refresh_token
                )

        self.assertEqual(status_code, status.HTTP_200_OK)

        # 無効となっているか
        self.assertEqual(card_access_auth.state, 9)

    def test_send_card_101_expired_success(self):
        # 予めアクセストークンを発行しておく
        test_repository: IAccessTokenRepository = IMockAccessTokenRepository()
        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute('9999999999990101', '0101')

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNotNone(access_token_response)

        access_token_payload_json = decode_token_to_json(
            access_token_response.access_token)
        refresh_token_payload_json = decode_token_to_json(
            access_token_response.refresh_token)

        self.assertEqual(
            access_token_payload_json['card_no'], '9999999999990101'
            )
        self.assertEqual(
            refresh_token_payload_json['card_no'], '9999999999990101'
            )

        card_access_auth = test_repository.get_card_access_authorization('9999999999990101')
        # 有効となっているか
        self.assertEqual(card_access_auth.state, 1)

        # 有効期限切れにする。
        card_access_auth.access_token_expire_at = 0

        # 失効
        invalidate_access_token = InvalidateAccessToken(test_repository)
        status_code = invalidate_access_token.execute(
                access_token_response.access_token,
                access_token_response.refresh_token
                )

        self.assertEqual(status_code, status.HTTP_200_OK)

        # 無効となっているか
        self.assertEqual(card_access_auth.state, 9)
