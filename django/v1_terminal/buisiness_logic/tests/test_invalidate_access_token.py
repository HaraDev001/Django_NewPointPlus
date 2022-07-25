from rest_framework import status
from django.test import SimpleTestCase
from v1_terminal.data.ITerminalAccessTokenRepository \
    import ITerminalAccessTokenRepository
from v1_terminal.data.IMockTerminalAccessTokenRepository \
    import IMockTerminalAccessTokenRepository
from v1_terminal.buisiness_logic.access_token.issue_access_token \
    import IssueAccessToken
from v1_terminal.buisiness_logic.access_token.invalidate_access_token \
    import InvalidateAccessToken

from v1_terminal.buisiness_logic.access_token.common import decode_token_to_json


class AccessTokenInvalidateTests(SimpleTestCase):

    # 店舗端末情報 [あり] メールアドレス・パスワード [一致] 事業者利用規約 [同意済] 店舗端末 [有効]
    # ユーザーは店舗端末を操作する権限を [持っている]
    def test_terminal_11111_success(self):
        # 予めアクセストークンを発行しておく
        test_repository: ITerminalAccessTokenRepository = \
            IMockTerminalAccessTokenRepository()

        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute(
                'terminal.01@example.co.jp', 'terminal.01.password', 'terminal_01')

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNotNone(access_token_response)

        access_token_payload_json = decode_token_to_json(
            access_token_response.access_token
        )
        mail_address = access_token_payload_json['mail_address']
        terminal_no = access_token_payload_json['terminal_no']

        terminal_access_auth = test_repository.get_terminal_access_authorization(
            mail_address, terminal_no
        )

        # 有効となっているか
        self.assertEqual(terminal_access_auth.state, 1)

        # 失効
        invalidate_access_token = InvalidateAccessToken(test_repository)
        status_code = invalidate_access_token.execute(
                access_token_response.access_token,
                access_token_response.refresh_token)

        self.assertEqual(status_code, status.HTTP_200_OK)

        # 無効となっているか
        self.assertEqual(terminal_access_auth.state, 9)

    def test_terminal_11111_expired_success(self):
        # 予めアクセストークンを発行しておく
        test_repository: ITerminalAccessTokenRepository = \
            IMockTerminalAccessTokenRepository()

        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute(
                'terminal.01@example.co.jp', 'terminal.01.password', 'terminal_01')

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNotNone(access_token_response)

        access_token_payload_json = decode_token_to_json(
            access_token_response.access_token
        )
        mail_address = access_token_payload_json['mail_address']
        terminal_no = access_token_payload_json['terminal_no']

        terminal_access_auth = test_repository.get_terminal_access_authorization(
            mail_address, terminal_no
        )

        # 有効となっているか
        self.assertEqual(terminal_access_auth.state, 1)

        # 有効期限切れにする。
        old_expired_at = terminal_access_auth.access_token_expire_at
        terminal_access_auth.access_token_expire_at = 0

        # 失効
        invalidate_access_token = InvalidateAccessToken(test_repository)
        status_code = invalidate_access_token.execute(
                access_token_response.access_token,
                access_token_response.refresh_token)

        self.assertEqual(status_code, status.HTTP_200_OK)

        # 無効となっているか
        self.assertEqual(terminal_access_auth.state, 9)

        # 有効期限をもとに戻す。
        terminal_access_auth.access_token_expire_at = old_expired_at
