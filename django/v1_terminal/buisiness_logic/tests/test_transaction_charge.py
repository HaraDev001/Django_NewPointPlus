from v1_terminal.data.ICardActivateRepository import ICardActivateRepository
from v1_terminal.data.IMockCardActivateRepository import IMockCardActivateRepository
from v1_terminal.data.ITerminalAccessTokenRepository import ITerminalAccessTokenRepository
from v1_terminal.data.IMockTerminalAccessTokenRepository import IMockTerminalAccessTokenRepository
from v1_terminal.data.ITransactionChargeRepository import ITransactionChargeRepository
from v1_terminal.data.IMockTransactionChargeRepository import IMockTransactionChargeRepository
from v1_terminal.buisiness_logic.transaction.transaction_charge import TransactionCharge
from v1_terminal.buisiness_logic.access_token.issue_access_token \
    import IssueAccessToken
from django.test import SimpleTestCase
from rest_framework import status

#フェーズ2でテスト項目を増やす
class TransactionChargeTests(SimpleTestCase):

    def test_charge_101_success(self):
        pk = '122348'
        card = {
            'card_no': '9999999999990103',
            'card_pin': '0103',
            'magnetic_information':'info'
        }
        charge_amount = 10000
        campaign_flag = {
            'sync': 0,
            'asynchronous': 1,
            'not_applicable': 0
        }

        terminal_repository: ITerminalAccessTokenRepository = \
            IMockTerminalAccessTokenRepository()

        issue_access_token = IssueAccessToken(terminal_repository)

        access_token_response, status_code = \
            issue_access_token.execute(
                'terminal.01@example.co.jp', 'terminal.01.password', 'terminal_01')

        access_token = access_token_response.access_token

        card_activate_repository: ICardActivateRepository = IMockCardActivateRepository()
        transaction_charge_repository: ITransactionChargeRepository = IMockTransactionChargeRepository()
        transaction_charge = \
            TransactionCharge(card_activate_repository, terminal_repository, transaction_charge_repository)
        charge, response_status = transaction_charge.execute(pk, card, access_token, charge_amount, campaign_flag)

        self.assertEqual(response_status, status.HTTP_200_OK)
        self.assertEqual(charge.card_transaction.transaction_after.value_transaction_balance, 11000)
        self.assertIsNotNone(charge)

