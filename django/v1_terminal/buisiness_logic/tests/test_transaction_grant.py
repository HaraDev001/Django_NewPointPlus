from v1_terminal.data.ICardActivateRepository import ICardActivateRepository
from v1_terminal.data.IMockCardActivateRepository import IMockCardActivateRepository
from v1_terminal.data.ITerminalAccessTokenRepository import ITerminalAccessTokenRepository
from v1_terminal.data.IMockTerminalAccessTokenRepository import IMockTerminalAccessTokenRepository
from v1_terminal.data.ITransactionChargeRepository import ITransactionChargeRepository
from v1_terminal.data.IMockTransactionGrantRepository import IMockTransactionGrantRepository
from v1_terminal.buisiness_logic.transaction.transaction_grant import TransactionGrant
from v1_terminal.buisiness_logic.access_token.issue_access_token \
    import IssueAccessToken
from django.test import SimpleTestCase
from rest_framework import status
from datetime import date

#フェーズ2でテスト項目を増やす
class TransactionGrantTests(SimpleTestCase):

    def test_grant101_success(self):
        pk = '122345'
        card_number = '9999999999990103'
        pin_number = '0103'
        grant_method = 0
        grant_account = '999999'
        amount = 100000
        expiration_date = date(2022, 1, 1)
        usage_restriction = {
            'usage_restriction_pattern': 0,
            'restriction_subject': [{
                'restricted_corporate_number': '100000',
                'restricted_shop_number': '999999999999999',
                'restricted_management_tags': '100000000000'
            }]
        }

        terminal_repository: ITerminalAccessTokenRepository = \
            IMockTerminalAccessTokenRepository()

        issue_access_token = IssueAccessToken(terminal_repository)

        access_token_response, status_code = \
            issue_access_token.execute(
                'terminal.01@example.co.jp', 'terminal.01.password', 'terminal_01')

        access_token = access_token_response.access_token

        card_activate_repository: ICardActivateRepository = IMockCardActivateRepository()
        transaction_grant_repository: ITransactionGrantRepository = IMockTransactionGrantRepository()
        transaction_grant = \
            TransactionGrant(card_activate_repository, terminal_repository, transaction_grant_repository)
        grant, response_status = transaction_grant.execute(pk, card_number, pin_number, access_token, amount,
                                                    grant_method, grant_account, usage_restriction)

        self.assertEqual(response_status, status.HTTP_200_OK)
        self.assertEqual(grant.card_transaction.transaction_after.payable_bonus_balance, 10000)
        self.assertIsNotNone(grant)