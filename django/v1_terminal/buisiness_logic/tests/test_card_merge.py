from rest_framework import status
from django.test import SimpleTestCase

from v1_card.data.IAccessTokenRepository import IAccessTokenRepository
from v1_card.data.IMockAccessTokenRepository import IMockAccessTokenRepository

from v1_terminal.data.ICardMergeRepository import ICardMergeRepository
from v1_terminal.data.IMockCardMergeRepository import IMockCardMergeRepository

from v1_terminal.data.ITerminalAccessTokenRepository \
    import ITerminalAccessTokenRepository
from v1_terminal.data.IMockTerminalAccessTokenRepository \
    import IMockTerminalAccessTokenRepository
from v1_terminal.buisiness_logic.access_token.issue_access_token \
    import IssueAccessToken

from v1_terminal.buisiness_logic.card.card_merge import CardMerge


class CardMergeTests(SimpleTestCase):

    def test_merge_value_charge_success(self):
        # 予めアクセストークンを発行しておく

        test_repository_card_access_token: IAccessTokenRepository = \
            IMockAccessTokenRepository()
        test_repository_terminal_access_token: ITerminalAccessTokenRepository = \
            IMockTerminalAccessTokenRepository()

        issue_access_token = IssueAccessToken(test_repository_terminal_access_token)

        test_repository_card_merge: \
            ICardMergeRepository = IMockCardMergeRepository(
                test_repository_card_access_token,
                test_repository_terminal_access_token
                )

        access_token_response, status_code = \
            issue_access_token.execute(
                'terminal.user.01@example.co.jp', 'terminal.user.01.password', '01-01-01-01')

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNotNone(access_token_response)

        merge_from = {'card_no': '9999999999990901', 'card_pin': '0901', 'magnetic_information': ''}
        merge_to = {'card_no': '9999999999990902', 'card_pin': '0902', 'magnetic_information': ''}

        card_merge = CardMerge(test_repository_card_merge)
        transaction_cancel_response, status_code = \
            card_merge.execute(access_token_response.access_token, merge_from, merge_to)

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNotNone(transaction_cancel_response)

    def test_merge_value_charge_over_limit_fail(self):
        # 予めアクセストークンを発行しておく

        test_repository_card_access_token: IAccessTokenRepository = \
            IMockAccessTokenRepository()
        test_repository_terminal_access_token: ITerminalAccessTokenRepository = \
            IMockTerminalAccessTokenRepository()

        issue_access_token = IssueAccessToken(test_repository_terminal_access_token)

        test_repository_card_merge: \
            ICardMergeRepository = IMockCardMergeRepository(
                test_repository_card_access_token,
                test_repository_terminal_access_token
                )

        access_token_response, status_code = \
            issue_access_token.execute(
                'terminal.user.01@example.co.jp', 'terminal.user.01.password', '01-01-01-01')

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNotNone(access_token_response)

        merge_from = {'card_no': '9999999999990901', 'card_pin': '0901', 'magnetic_information': ''}
        merge_to = {'card_no': '9999999999990903', 'card_pin': '0903', 'magnetic_information': ''}

        card_merge = CardMerge(test_repository_card_merge)
        transaction_cancel_response, status_code = \
            card_merge.execute(access_token_response.access_token, merge_from, merge_to)

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNone(transaction_cancel_response)

    def test_merge_bonus_same_card_config_success(self):
        # 予めアクセストークンを発行しておく

        test_repository_card_access_token: IAccessTokenRepository = \
            IMockAccessTokenRepository()
        test_repository_terminal_access_token: ITerminalAccessTokenRepository = \
            IMockTerminalAccessTokenRepository()

        issue_access_token = IssueAccessToken(test_repository_terminal_access_token)

        test_repository_card_merge: \
            ICardMergeRepository = IMockCardMergeRepository(
                test_repository_card_access_token,
                test_repository_terminal_access_token
                )

        access_token_response, status_code = \
            issue_access_token.execute(
                'terminal.user.01@example.co.jp', 'terminal.user.01.password', '01-01-01-01')

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNotNone(access_token_response)

        merge_from = {'card_no': '9999999999990904', 'card_pin': '0904', 'magnetic_information': ''}
        merge_to = {'card_no': '9999999999990905', 'card_pin': '0905', 'magnetic_information': ''}

        card_merge = CardMerge(test_repository_card_merge)
        transaction_cancel_response, status_code = \
            card_merge.execute(access_token_response.access_token, merge_from, merge_to)

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNotNone(transaction_cancel_response)

    def test_merge_bonus_deferent_card_config_success(self):
        # 予めアクセストークンを発行しておく

        test_repository_card_access_token: IAccessTokenRepository = \
            IMockAccessTokenRepository()
        test_repository_terminal_access_token: ITerminalAccessTokenRepository = \
            IMockTerminalAccessTokenRepository()

        issue_access_token = IssueAccessToken(test_repository_terminal_access_token)

        test_repository_card_merge: \
            ICardMergeRepository = IMockCardMergeRepository(
                test_repository_card_access_token,
                test_repository_terminal_access_token
                )

        access_token_response, status_code = \
            issue_access_token.execute(
                'terminal.user.01@example.co.jp', 'terminal.user.01.password', '01-01-01-01')

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNotNone(access_token_response)

        merge_from = {'card_no': '9999999999990904', 'card_pin': '0904', 'magnetic_information': ''}
        merge_to = {'card_no': '9999999999990901', 'card_pin': '0901', 'magnetic_information': ''}

        card_merge = CardMerge(test_repository_card_merge)
        transaction_cancel_response, status_code = \
            card_merge.execute(access_token_response.access_token, merge_from, merge_to)

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNotNone(transaction_cancel_response)

    def test_merge_bonus_over_limit_fail(self):
        # 予めアクセストークンを発行しておく

        test_repository_card_access_token: IAccessTokenRepository = \
            IMockAccessTokenRepository()
        test_repository_terminal_access_token: ITerminalAccessTokenRepository = \
            IMockTerminalAccessTokenRepository()

        issue_access_token = IssueAccessToken(test_repository_terminal_access_token)

        test_repository_card_merge: \
            ICardMergeRepository = IMockCardMergeRepository(
                test_repository_card_access_token,
                test_repository_terminal_access_token
                )

        access_token_response, status_code = \
            issue_access_token.execute(
                'terminal.user.01@example.co.jp', 'terminal.user.01.password', '01-01-01-01')

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNotNone(access_token_response)

        merge_from = {'card_no': '9999999999990905', 'card_pin': '0905', 'magnetic_information': ''}
        merge_to = {'card_no': '9999999999990906', 'card_pin': '0906', 'magnetic_information': ''}

        card_merge = CardMerge(test_repository_card_merge)
        transaction_cancel_response, status_code = \
            card_merge.execute(access_token_response.access_token, merge_from, merge_to)

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNone(transaction_cancel_response)
