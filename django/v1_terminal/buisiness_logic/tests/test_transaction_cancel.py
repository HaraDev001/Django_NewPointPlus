from rest_framework import status
from django.test import SimpleTestCase

from v1_card.data.IAccessTokenRepository import IAccessTokenRepository
from v1_card.data.IMockAccessTokenRepository import IMockAccessTokenRepository

from v1_terminal.data.ITransactionCancelRepository \
    import ITransactionCancelRepository
from v1_terminal.data.IMockTransactionCancelRepository \
    import IMockTransactionCancelRepository
from v1_terminal.buisiness_logic.terminal.transaction_cancel \
    import CancelTransaction
from v1_terminal.data.ITerminalAccessTokenRepository \
    import ITerminalAccessTokenRepository
from v1_terminal.data.IMockTerminalAccessTokenRepository \
    import IMockTerminalAccessTokenRepository
from v1_terminal.buisiness_logic.access_token.issue_access_token \
    import IssueAccessToken


class TransactionCancelTests(SimpleTestCase):

    def test_cancel_value_charge_success(self):
        # 予めアクセストークンを発行しておく

        test_repository_card_access_token: IAccessTokenRepository = \
            IMockAccessTokenRepository()
        test_repository_terminal_access_token: ITerminalAccessTokenRepository = \
            IMockTerminalAccessTokenRepository()

        issue_access_token = IssueAccessToken(test_repository_terminal_access_token)

        test_repository_cancel_transaction: \
            ITransactionCancelRepository = IMockTransactionCancelRepository(
                test_repository_card_access_token,
                test_repository_terminal_access_token
                )

        access_token_response, status_code = \
            issue_access_token.execute(
                'terminal.user.01@example.co.jp', 'terminal.user.01.password', '01-01-01-01')

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNotNone(access_token_response)

        cancel_transaction = CancelTransaction(test_repository_cancel_transaction)

        transaction_cancel_response, status_code = cancel_transaction.execute(
            access_token_response.access_token, '9999999999990901', '0901',
            None, 'de4bfd79-204a-49d8-aa09-7851992972ac', '9d2af7aa-cbc1-42f7-88c6-e71f3e08ee72')

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNotNone(transaction_cancel_response)

    def test_cancel_value_charge_fail(self):
        # 予めアクセストークンを発行しておく

        test_repository_card_access_token: IAccessTokenRepository = \
            IMockAccessTokenRepository()
        test_repository_terminal_access_token: ITerminalAccessTokenRepository = \
            IMockTerminalAccessTokenRepository()

        issue_access_token = IssueAccessToken(test_repository_terminal_access_token)

        test_repository_cancel_transaction: \
            ITransactionCancelRepository = IMockTransactionCancelRepository(
                test_repository_card_access_token,
                test_repository_terminal_access_token
                )

        access_token_response, status_code = \
            issue_access_token.execute(
                'terminal.user.01@example.co.jp', 'terminal.user.01.password', '01-01-01-01')

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNotNone(access_token_response)

        cancel_transaction = CancelTransaction(test_repository_cancel_transaction)

        transaction_cancel_response, status_code = cancel_transaction.execute(
            access_token_response.access_token, '9999999999990902', '0902',
            None, 'de4bfd79-204a-49d8-aa09-7851992972ac', '9dca6863-8c9a-413d-8e98-85f688c57353')

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNone(transaction_cancel_response)

    def test_cancel_pay_success(self):
        # 予めアクセストークンを発行しておく

        test_repository_card_access_token: IAccessTokenRepository = \
            IMockAccessTokenRepository()
        test_repository_terminal_access_token: ITerminalAccessTokenRepository = \
            IMockTerminalAccessTokenRepository()

        issue_access_token = IssueAccessToken(test_repository_terminal_access_token)

        test_repository_cancel_transaction: \
            ITransactionCancelRepository = IMockTransactionCancelRepository(
                test_repository_card_access_token,
                test_repository_terminal_access_token
                )

        access_token_response, status_code = \
            issue_access_token.execute(
                'terminal.user.01@example.co.jp', 'terminal.user.01.password', '01-01-01-01')

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNotNone(access_token_response)

        cancel_transaction = CancelTransaction(test_repository_cancel_transaction)

        transaction_cancel_response, status_code = cancel_transaction.execute(
            access_token_response.access_token, '9999999999990902', '0902',
            None, 'de4bfd79-204a-49d8-aa09-7851992972ac', '2e1d2a90-e2f7-416c-a7c0-5911d43aa6b7')

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNotNone(transaction_cancel_response)

    def test_cancel_grant_payable_bonus_success(self):
        # 予めアクセストークンを発行しておく

        test_repository_card_access_token: IAccessTokenRepository = \
            IMockAccessTokenRepository()
        test_repository_terminal_access_token: ITerminalAccessTokenRepository = \
            IMockTerminalAccessTokenRepository()

        issue_access_token = IssueAccessToken(test_repository_terminal_access_token)

        test_repository_cancel_transaction: \
            ITransactionCancelRepository = IMockTransactionCancelRepository(
                test_repository_card_access_token,
                test_repository_terminal_access_token
                )

        access_token_response, status_code = \
            issue_access_token.execute(
                'terminal.user.01@example.co.jp', 'terminal.user.01.password', '01-01-01-01')

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNotNone(access_token_response)

        cancel_transaction = CancelTransaction(test_repository_cancel_transaction)

        transaction_cancel_response, status_code = cancel_transaction.execute(
            access_token_response.access_token, '9999999999990902', '0902',
            None, 'de4bfd79-204a-49d8-aa09-7851992972ac', '052a3dc8-04e6-4584-ba07-af792fd44fc1')

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNotNone(transaction_cancel_response)

    def test_cancel_use_payable_bonus_success(self):
        # 予めアクセストークンを発行しておく

        test_repository_card_access_token: IAccessTokenRepository = \
            IMockAccessTokenRepository()
        test_repository_terminal_access_token: ITerminalAccessTokenRepository = \
            IMockTerminalAccessTokenRepository()

        issue_access_token = IssueAccessToken(test_repository_terminal_access_token)

        test_repository_cancel_transaction: \
            ITransactionCancelRepository = IMockTransactionCancelRepository(
                test_repository_card_access_token,
                test_repository_terminal_access_token
                )

        access_token_response, status_code = \
            issue_access_token.execute(
                'terminal.user.01@example.co.jp', 'terminal.user.01.password', '01-01-01-01')

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNotNone(access_token_response)

        cancel_transaction = CancelTransaction(test_repository_cancel_transaction)

        transaction_cancel_response, status_code = cancel_transaction.execute(
            access_token_response.access_token, '9999999999990902', '0902',
            None, 'de4bfd79-204a-49d8-aa09-7851992972ac', 'cb1fb51a-f495-4a14-8c09-43b12a84109f')

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNotNone(transaction_cancel_response)
