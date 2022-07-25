from v1_terminal.data.ITerminalAccessTokenRepository import ITerminalAccessTokenRepository
from v1_terminal.data.IMockTerminalAccessTokenRepository import IMockTerminalAccessTokenRepository
from v1_terminal.data.IMockTransactionSummaryRepository import IMockTransactionSummaryRepository
from v1_terminal.buisiness_logic.transaction.transaction_summary import TransactionSummary
from v1_terminal.buisiness_logic.access_token.issue_access_token \
    import IssueAccessToken
from django.test import SimpleTestCase
from rest_framework import status
from datetime import date

#フェーズ2でテスト項目を増やす
class TransactionSummaryTests(SimpleTestCase):
    def test_summary101_success(self):
        search = {
            'search_date':{
                'start_aggregation_at': date(2020, 12, 30),
                'end_aggregation_at': date(2021, 12, 30),
            },
            'terminal_number': 'terminal_01'
        }

        terminal_repository: ITerminalAccessTokenRepository = \
            IMockTerminalAccessTokenRepository()

        issue_access_token = IssueAccessToken(terminal_repository)

        access_token_response, status_code = \
            issue_access_token.execute(
                'terminal.01@example.co.jp', 'terminal.01.password', 'terminal_01')

        access_token = access_token_response.access_token

        transaction_summary_repository: ITransactionSummaryRepository = IMockTransactionSummaryRepository()
        transaction_summary = \
            TransactionSummary(terminal_repository, transaction_summary_repository)
        summary, response_status = transaction_summary.execute(access_token, search)

        self.assertEqual(response_status, status.HTTP_200_OK)
        self.assertEqual(summary.charge.total_amount, 10000)
        self.assertIsNotNone(summary)

    #検索日時外
    def test_summary102_date_fail(self):
        search = {
            'search_date':{
                'start_aggregation_at': date(2020, 12, 30),
                'end_aggregation_at': date(2021, 4, 30),
            },
            'terminal_number': 'terminal_01'
        }

        terminal_repository: ITerminalAccessTokenRepository = \
            IMockTerminalAccessTokenRepository()

        issue_access_token = IssueAccessToken(terminal_repository)

        access_token_response, status_code = \
            issue_access_token.execute(
                'terminal.01@example.co.jp', 'terminal.01.password', 'terminal_01')

        access_token = access_token_response.access_token

        transaction_summary_repository: ITransactionSummaryRepository = IMockTransactionSummaryRepository()
        transaction_summary = \
            TransactionSummary(terminal_repository, transaction_summary_repository)
        summary, response_status = transaction_summary.execute(access_token, search)

        self.assertEqual(response_status, status.HTTP_400_BAD_REQUEST)
        self.assertIsNone(summary)

    #検索日時外
    def test_summary103_terminal_fail(self):
        search = {
            'search_date':{
                'start_aggregation_at': date(2020, 12, 30),
                'end_aggregation_at': date(2021, 12, 30),
            },
            'terminal_number': 'terminal_02'
        }

        terminal_repository: ITerminalAccessTokenRepository = \
            IMockTerminalAccessTokenRepository()

        issue_access_token = IssueAccessToken(terminal_repository)

        access_token_response, status_code = \
            issue_access_token.execute(
                'terminal.01@example.co.jp', 'terminal.01.password', 'terminal_01')

        access_token = access_token_response.access_token

        transaction_summary_repository: ITransactionSummaryRepository = IMockTransactionSummaryRepository()
        transaction_summary = \
            TransactionSummary(terminal_repository, transaction_summary_repository)
        summary, response_status = transaction_summary.execute(access_token, search)

        self.assertEqual(response_status, status.HTTP_400_BAD_REQUEST)
        self.assertIsNone(summary)