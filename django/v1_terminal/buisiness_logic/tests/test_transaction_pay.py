from v1_terminal.data.ICardActivateRepository import ICardActivateRepository
from v1_terminal.data.IMockCardActivateRepository import IMockCardActivateRepository
from v1_terminal.data.ITerminalAccessTokenRepository import ITerminalAccessTokenRepository
from v1_terminal.data.IMockTerminalAccessTokenRepository import IMockTerminalAccessTokenRepository
from v1_terminal.data.ITransactionChargeRepository import ITransactionChargeRepository
from v1_terminal.data.IMockTransactionPayRepository import IMockTransactionPayRepository
from v1_terminal.buisiness_logic.transaction.transaction_pay import TransactionPay
from v1_terminal.buisiness_logic.access_token.issue_access_token \
    import IssueAccessToken
from django.test import SimpleTestCase
from rest_framework import status

#フェーズ2でテスト項目を増やす
class TransactionPayTests(SimpleTestCase):

    def test_pay101_success(self):
        pk = '122345'
        card = [
            {
                'card_no': '9999999999990103',
                'card_pin': '0103',
                'magnetic_information':'info',
                'used_payment_bonus':{
                    'used_payment_bonus_number': 1000
                }
            }
        ]
        payment_amount = 10000
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
        transaction_pay_repository: ITransactionPayRepository = IMockTransactionPayRepository()
        transaction_pay = \
            TransactionPay(card_activate_repository, terminal_repository, transaction_pay_repository)
        payment, response_status = transaction_pay.execute(pk, card, access_token, payment_amount, campaign_flag)

        self.assertEqual(response_status, status.HTTP_200_OK)
        self.assertEqual(payment.card_transaction[0].transaction_after.value_transaction_balance, 9000)
        self.assertIsNotNone(payment)