# from unittest import mock
from rest_framework import status
from django.test import SimpleTestCase
from v1_terminal.data.ITerminalAccessTokenRepository import ITerminalAccessTokenRepository
from v1_terminal.data.IMockTerminalAccessTokenRepository import IMockTerminalAccessTokenRepository
from v1_terminal.buisiness_logic.access_token.issue_access_token \
    import IssueAccessToken
from v1_terminal.buisiness_logic.access_token.common \
    import decode_token_to_json
from utils.datetime_utility import (now,
                                    to_utc_timestamp,
                                    get_datetime_hours_later_from
                                    )


class AccessTokenIssueTests(SimpleTestCase):

    # 店舗端末情報 [あり] メールアドレス・パスワード [一致] 事業者利用規約 [同意済] 店舗端末 [有効]
    # ユーザーは店舗端末を操作する権限を [持っている]
    def test_terminal_11111_success(self):

        test_repository: ITerminalAccessTokenRepository = \
            IMockTerminalAccessTokenRepository()

        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute(
                'terminal.01@example.co.jp', 'terminal.01.password', 'terminal_01')

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNotNone(access_token_response)

        access_token_payload_json = decode_token_to_json(
            access_token_response.access_token)

        self.assertEqual(
            access_token_payload_json['mail_address'], 'terminal.01@example.co.jp'
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
            refresh_token_payload_json['mail_address'], 'terminal.01@example.co.jp'
            )

    # 店舗端末情報 [あり] メールアドレス・パスワード [不一致] 事業者利用規約 [同意済] 店舗端末 [有効]
    # ユーザーは店舗端末を操作する権限を [持っている]
    def test_terminal_10111_fail(self):

        test_repository: ITerminalAccessTokenRepository = \
            IMockTerminalAccessTokenRepository()

        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute(
                'terminal.01@example.co.jp', 'XXXXXX', 'terminal_01')

        # アクセストークンの発行はない
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNone(access_token_response)

    # 店舗端末情報 [あり] メールアドレス・パスワード [一致] 事業者利用規約 [未同意] 店舗端末 [有効]
    # ユーザーは店舗端末を操作する権限を [持っている]
    def test_terminal_11011_fail(self):

        test_repository: ITerminalAccessTokenRepository = \
            IMockTerminalAccessTokenRepository()

        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute(
                'terminal.01@example.co.jp', 'terminal.01.password', 'terminal_03')

        # アクセストークンの発行はない
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNone(access_token_response)

    # 店舗端末情報 [あり] メールアドレス・パスワード [一致] 事業者利用規約 [同意済] 店舗端末 [無効]
    # ユーザーは店舗端末を操作する権限を [持っている]
    def test_terminal_11101_fail(self):

        test_repository: ITerminalAccessTokenRepository = \
            IMockTerminalAccessTokenRepository()

        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute(
                'terminal.01@example.co.jp', 'terminal.01.password', 'terminal_02')

        # アクセストークンの発行はない
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNone(access_token_response)

    # 店舗端末情報 [あり] メールアドレス・パスワード [一致] 事業者利用規約 [同意済] 店舗端末 [有効]
    # ユーザーは店舗端末を操作する権限を [持ってない]
    def test_terminal_11110_fail(self):

        test_repository: ITerminalAccessTokenRepository = \
            IMockTerminalAccessTokenRepository()

        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute(
                'terminal.02@example.co.jp', 'terminal.02.password', 'terminal_01')

        # アクセストークンの発行はない
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNone(access_token_response)

    # 店舗端末情報 [あり] メールアドレス・パスワード [不一致] 事業者利用規約 [未同意] 店舗端末 [有効]
    # ユーザーは店舗端末を操作する権限を [持っている]
    def test_terminal_10011_fail(self):

        test_repository: ITerminalAccessTokenRepository = \
            IMockTerminalAccessTokenRepository()

        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute(
                'terminal.01@example.co.jp', 'XXXXX', 'terminal_01')

        # アクセストークンの発行はない
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNone(access_token_response)

    # 店舗端末情報 [あり] メールアドレス・パスワード [不一致] 事業者利用規約 [同意済] 店舗端末 [無効]
    # ユーザーは店舗端末を操作する権限を [持っている]
    def test_terminal_10101_fail(self):

        test_repository: ITerminalAccessTokenRepository = \
            IMockTerminalAccessTokenRepository()

        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute(
                'terminal.01@example.co.jp', 'XXXXX', 'terminal_02')

        # アクセストークンの発行はない
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNone(access_token_response)

    # 店舗端末情報 [あり] メールアドレス・パスワード [不一致] 事業者利用規約 [同意済] 店舗端末 [有効]
    # ユーザーは店舗端末を操作する権限を [持ってない]
    def test_terminal_10110_fail(self):

        test_repository: ITerminalAccessTokenRepository = \
            IMockTerminalAccessTokenRepository()

        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute(
                'terminal.02@example.co.jp', 'XXXXX', 'terminal_01')

        # アクセストークンの発行はない
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNone(access_token_response)

    # 店舗端末情報 [あり] メールアドレス・パスワード [一致] 事業者利用規約 [未同意] 店舗端末 [無効]
    # ユーザーは店舗端末を操作する権限を [持っている]
    def test_terminal_11001_fail(self):

        test_repository: ITerminalAccessTokenRepository = \
            IMockTerminalAccessTokenRepository()

        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute(
                'terminal.01@example.co.jp', 'terminal.01.password', 'terminal_04')

        # アクセストークンの発行はない
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNone(access_token_response)

    # 店舗端末情報 [あり] メールアドレス・パスワード [一致] 事業者利用規約 [未同意] 店舗端末 [有効]
    # ユーザーは店舗端末を操作する権限を [持ってない]
    def test_terminal_11010_fail(self):

        test_repository: ITerminalAccessTokenRepository = \
            IMockTerminalAccessTokenRepository()

        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute(
                'terminal.02@example.co.jp', 'terminal.02.password', 'terminal_03')

        # アクセストークンの発行はない
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNone(access_token_response)

    # 店舗端末情報 [あり] メールアドレス・パスワード [一致] 事業者利用規約 [同意済] 店舗端末 [無効]
    # ユーザーは店舗端末を操作する権限を [持ってない]
    def test_terminal_11100_fail(self):

        test_repository: ITerminalAccessTokenRepository = \
            IMockTerminalAccessTokenRepository()

        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute(
                'terminal.02@example.co.jp', 'terminal.02.password', 'terminal_02')

        # アクセストークンの発行はない
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNone(access_token_response)

    # 店舗端末情報 [あり] メールアドレス・パスワード [不一致] 事業者利用規約 [未同意] 店舗端末 [無効]
    # ユーザーは店舗端末を操作する権限を [持っている]
    def test_terminal_10001_fail(self):

        test_repository: ITerminalAccessTokenRepository = \
            IMockTerminalAccessTokenRepository()

        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute(
                'terminal.01@example.co.jp', 'XXXXX', 'terminal_04')

        # アクセストークンの発行はない
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNone(access_token_response)

    # 店舗端末情報 [あり] メールアドレス・パスワード [不一致] 事業者利用規約 [未同意] 店舗端末 [有効]
    # ユーザーは店舗端末を操作する権限を [持ってない]
    def test_terminal_10010_fail(self):

        test_repository: ITerminalAccessTokenRepository = \
            IMockTerminalAccessTokenRepository()

        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute(
                'terminal.02@example.co.jp', 'XXXXX', 'terminal_03')

        # アクセストークンの発行はない
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNone(access_token_response)

    # 店舗端末情報 [あり] メールアドレス・パスワード [不一致] 事業者利用規約 [同意済] 店舗端末 [無効]
    # ユーザーは店舗端末を操作する権限を [持ってない]
    def test_terminal_10100_fail(self):

        test_repository: ITerminalAccessTokenRepository = \
            IMockTerminalAccessTokenRepository()

        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute(
                'terminal.02@example.co.jp', 'XXXXX', 'terminal_02')

        # アクセストークンの発行はない
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNone(access_token_response)

    # 店舗端末情報 [あり] メールアドレス・パスワード [一致] 事業者利用規約 [未同意] 店舗端末 [無効]
    # ユーザーは店舗端末を操作する権限を [持ってない]
    def test_terminal_11000_fail(self):

        test_repository: ITerminalAccessTokenRepository = \
            IMockTerminalAccessTokenRepository()

        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute(
                'terminal.02@example.co.jp', 'terminal.02.password', 'terminal_04')

        # アクセストークンの発行はない
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNone(access_token_response)

    # 店舗端末情報 [あり] メールアドレス・パスワード [不一致] 事業者利用規約 [未同意] 店舗端末 [無効]
    # ユーザーは店舗端末を操作する権限を [持ってない]
    def test_terminal_10000_fail(self):

        test_repository: ITerminalAccessTokenRepository = \
            IMockTerminalAccessTokenRepository()

        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute(
                'terminal.02@example.co.jp', 'XXXXX', 'terminal_04')

        # アクセストークンの発行はない
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNone(access_token_response)

    # ----------------------------------------------------------------------------------------------

    # 店舗端末情報 [なし] メールアドレス・パスワード [一致] 事業者利用規約 [同意済] 店舗端末 [有効]
    # ユーザーは店舗端末を操作する権限を [持っている]
    def test_terminal_01111_success(self):

        test_repository: ITerminalAccessTokenRepository = \
            IMockTerminalAccessTokenRepository()

        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute(
                'terminal.01@example.co.jp', 'terminal.01.password', 'terminal_XX')

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNone(access_token_response)

    # 店舗端末情報 [なし] メールアドレス・パスワード [不一致] 事業者利用規約 [同意済] 店舗端末 [有効]
    # ユーザーは店舗端末を操作する権限を [持っている]
    def test_terminal_00111_fail(self):

        test_repository: ITerminalAccessTokenRepository = \
            IMockTerminalAccessTokenRepository()

        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute(
                'terminal.01@example.co.jp', 'XXXXXX', 'terminal_XX')

        # アクセストークンの発行はない
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNone(access_token_response)

    # 店舗端末情報 [なし] メールアドレス・パスワード [一致] 事業者利用規約 [未同意] 店舗端末 [有効]
    # ユーザーは店舗端末を操作する権限を [持っている]
    def test_terminal_01011_fail(self):

        test_repository: ITerminalAccessTokenRepository = \
            IMockTerminalAccessTokenRepository()

        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute(
                'terminal.01@example.co.jp', 'terminal.01.password', 'terminal_XX')

        # アクセストークンの発行はない
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNone(access_token_response)

    # 店舗端末情報 [なし] メールアドレス・パスワード [一致] 事業者利用規約 [同意済] 店舗端末 [無効]
    # ユーザーは店舗端末を操作する権限を [持っている]
    def test_terminal_01101_fail(self):

        test_repository: ITerminalAccessTokenRepository = \
            IMockTerminalAccessTokenRepository()

        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute(
                'terminal.01@example.co.jp', 'terminal.01.password', 'terminal_XX')

        # アクセストークンの発行はない
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNone(access_token_response)

    # 店舗端末情報 [なし] メールアドレス・パスワード [一致] 事業者利用規約 [同意済] 店舗端末 [有効]
    # ユーザーは店舗端末を操作する権限を [持ってない]
    def test_terminal_01110_fail(self):

        test_repository: ITerminalAccessTokenRepository = \
            IMockTerminalAccessTokenRepository()

        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute(
                'terminal.02@example.co.jp', 'terminal.02.password', 'terminal_XX')

        # アクセストークンの発行はない
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNone(access_token_response)

    # 店舗端末情報 [なし] メールアドレス・パスワード [不一致] 事業者利用規約 [未同意] 店舗端末 [有効]
    # ユーザーは店舗端末を操作する権限を [持っている]
    def test_terminal_00011_fail(self):

        test_repository: ITerminalAccessTokenRepository = \
            IMockTerminalAccessTokenRepository()

        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute(
                'terminal.01@example.co.jp', 'XXXXX', 'terminal_XX')

        # アクセストークンの発行はない
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNone(access_token_response)

    # 店舗端末情報 [なし] メールアドレス・パスワード [不一致] 事業者利用規約 [同意済] 店舗端末 [無効]
    # ユーザーは店舗端末を操作する権限を [持っている]
    def test_terminal_00101_fail(self):

        test_repository: ITerminalAccessTokenRepository = \
            IMockTerminalAccessTokenRepository()

        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute(
                'terminal.01@example.co.jp', 'XXXXX', 'terminal_XX')

        # アクセストークンの発行はない
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNone(access_token_response)

    # 店舗端末情報 [なし] メールアドレス・パスワード [不一致] 事業者利用規約 [同意済] 店舗端末 [有効]
    # ユーザーは店舗端末を操作する権限を [持ってない]
    def test_terminal_00110_fail(self):

        test_repository: ITerminalAccessTokenRepository = \
            IMockTerminalAccessTokenRepository()

        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute(
                'terminal.02@example.co.jp', 'XXXXX', 'terminal_XX')

        # アクセストークンの発行はない
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNone(access_token_response)

    # 店舗端末情報 [なし] メールアドレス・パスワード [一致] 事業者利用規約 [未同意] 店舗端末 [無効]
    # ユーザーは店舗端末を操作する権限を [持っている]
    def test_terminal_01001_fail(self):

        test_repository: ITerminalAccessTokenRepository = \
            IMockTerminalAccessTokenRepository()

        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute(
                'terminal.01@example.co.jp', 'terminal.01.password', 'terminal_XX')

        # アクセストークンの発行はない
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNone(access_token_response)

    # 店舗端末情報 [なし] メールアドレス・パスワード [一致] 事業者利用規約 [未同意] 店舗端末 [有効]
    # ユーザーは店舗端末を操作する権限を [持ってない]
    def test_terminal_01010_fail(self):

        test_repository: ITerminalAccessTokenRepository = \
            IMockTerminalAccessTokenRepository()

        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute(
                'terminal.02@example.co.jp', 'terminal.02.password', 'terminal_XX')

        # アクセストークンの発行はない
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNone(access_token_response)

    # 店舗端末情報 [なし] メールアドレス・パスワード [一致] 事業者利用規約 [同意済] 店舗端末 [無効]
    # ユーザーは店舗端末を操作する権限を [持ってない]
    def test_terminal_01100_fail(self):

        test_repository: ITerminalAccessTokenRepository = \
            IMockTerminalAccessTokenRepository()

        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute(
                'terminal.02@example.co.jp', 'terminal.02.password', 'terminal_XX')

        # アクセストークンの発行はない
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNone(access_token_response)

    # 店舗端末情報 [なし] メールアドレス・パスワード [不一致] 事業者利用規約 [未同意] 店舗端末 [無効]
    # ユーザーは店舗端末を操作する権限を [持っている]
    def test_terminal_00001_fail(self):

        test_repository: ITerminalAccessTokenRepository = \
            IMockTerminalAccessTokenRepository()

        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute(
                'terminal.01@example.co.jp', 'XXXXX', 'terminal_XX')

        # アクセストークンの発行はない
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNone(access_token_response)

    # 店舗端末情報 [なし] メールアドレス・パスワード [不一致] 事業者利用規約 [未同意] 店舗端末 [有効]
    # ユーザーは店舗端末を操作する権限を [持ってない]
    def test_terminal_00010_fail(self):

        test_repository: ITerminalAccessTokenRepository = \
            IMockTerminalAccessTokenRepository()

        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute(
                'terminal.02@example.co.jp', 'XXXXX', 'terminal_XX')

        # アクセストークンの発行はない
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNone(access_token_response)

    # 店舗端末情報 [なし] メールアドレス・パスワード [不一致] 事業者利用規約 [同意済] 店舗端末 [無効]
    # ユーザーは店舗端末を操作する権限を [持ってない]
    def test_terminal_00100_fail(self):

        test_repository: ITerminalAccessTokenRepository = \
            IMockTerminalAccessTokenRepository()

        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute(
                'terminal.02@example.co.jp', 'XXXXX', 'terminal_XX')

        # アクセストークンの発行はない
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNone(access_token_response)

    # 店舗端末情報 [なし] メールアドレス・パスワード [一致] 事業者利用規約 [未同意] 店舗端末 [無効]
    # ユーザーは店舗端末を操作する権限を [持ってない]
    def test_terminal_01000_fail(self):

        test_repository: ITerminalAccessTokenRepository = \
            IMockTerminalAccessTokenRepository()

        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute(
                'terminal.02@example.co.jp', 'terminal.02.password', 'terminal_XX')

        # アクセストークンの発行はない
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNone(access_token_response)

    # 店舗端末情報 [なし] メールアドレス・パスワード [不一致] 事業者利用規約 [未同意] 店舗端末 [無効]
    # ユーザーは店舗端末を操作する権限を [持ってない]
    def test_terminal_00000_fail(self):

        test_repository: ITerminalAccessTokenRepository = \
            IMockTerminalAccessTokenRepository()

        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute(
                'terminal.02@example.co.jp', 'XXXXX', 'terminal_XX')

        # アクセストークンの発行はない
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNone(access_token_response)
