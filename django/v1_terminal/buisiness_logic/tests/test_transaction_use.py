from v1_terminal.data.ICardActivateRepository import ICardActivateRepository
from v1_terminal.data.IMockCardActivateRepository import IMockCardActivateRepository
from v1_terminal.data.ITerminalAccessTokenRepository import ITerminalAccessTokenRepository
from v1_terminal.data.IMockTerminalAccessTokenRepository import IMockTerminalAccessTokenRepository
from v1_terminal.data.ITransactionChargeRepository import ITransactionChargeRepository
from v1_terminal.data.IMockTransactionUseRepository import IMockTransactionUseRepository
from v1_terminal.buisiness_logic.transaction.transaction_use import TransactionUse
from v1_terminal.buisiness_logic.access_token.issue_access_token \
    import IssueAccessToken
from django.test import SimpleTestCase
from rest_framework import status

#フェーズ2でテスト項目を増やす
class TransactionUseTests(SimpleTestCase):

    def test_use101_success(self):
        pk = '122345'
        card = [
            {
                'card_no': '9999999999990103',
                'card_pin': '0103',
                'magnetic_information':'info',
                'product_exchange_bonus_used_number': 1000
            }
        ]

        terminal_repository: ITerminalAccessTokenRepository = \
            IMockTerminalAccessTokenRepository()

        issue_access_token = IssueAccessToken(terminal_repository)

        access_token_response, status_code = \
            issue_access_token.execute(
                'terminal.01@example.co.jp', 'terminal.01.password', 'terminal_01')

        access_token = access_token_response.access_token

        card_activate_repository: ICardActivateRepository = IMockCardActivateRepository()
        transaction_use_repository: ITransactionUseRepository = IMockTransactionUseRepository()
        transaction_use = \
            TransactionUse(card_activate_repository, terminal_repository, transaction_use_repository)
        use_bonus, response_status = transaction_use.execute(pk, card, access_token)

        self.assertEqual(response_status, status.HTTP_200_OK)
        self.assertEqual(use_bonus.card_transaction[0].transaction_after.product_exchange_bonus_balance, 9000)
        self.assertIsNotNone(use_bonus)