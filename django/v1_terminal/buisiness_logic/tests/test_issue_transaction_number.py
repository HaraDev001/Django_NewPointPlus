from django.test import SimpleTestCase
from rest_framework import status
from v1_terminal.buisiness_logic.transaction.issue_transaction_number import \
    IssueTransactionNumber
from v1_terminal.data.IIssueTransactionNumberReposiotry import \
    IIssueTransactionNumberRepository
from v1_terminal.data.IMockIssueTransactionNumberRepository import \
    IMockIssueTransactionnNumberRepository


class IssueTransactionTests(SimpleTestCase):

    def test_transaction_1_success(self):
        '''
        正常系
        '''

        test_repository: IIssueTransactionNumberRepository =\
            IMockIssueTransactionnNumberRepository()
        issue_transaction_number = IssueTransactionNumber(test_repository)
        transactions = test_repository.transactions
        # transactionsは空
        self.assertEqual(transactions, {})
        instance, status_code = issue_transaction_number.execute(
            "header.payload.terminal_1")
        self.assertIsNotNone(instance)
        self.assertEqual(status_code, status.HTTP_200_OK)
        # transactionsに発行した取引番号でのレコードが保存されている。
        self.assertIsNotNone(transactions.get(instance.transaction_number))

    def test_transaction_2_failure(self):
        '''
        current_unixtime > terminal_authorization.access_token_expires_at,
        トークン有効期限切れ
        '''

        test_repository: IIssueTransactionNumberRepository =\
            IMockIssueTransactionnNumberRepository()
        issue_transaction_number = IssueTransactionNumber(test_repository)
        instance, status_code = issue_transaction_number.execute(
            "header.payload.terminal_2")
        self.assertIsNone(instance)
        self.assertEqual(status_code, status.HTTP_400_BAD_REQUEST)

    def test_wrong_access_token_failure(self):
        '''
        認証トークンが店舗端末認証情報のレコードと不一致
        '''

        test_repository: IIssueTransactionNumberRepository =\
            IMockIssueTransactionnNumberRepository()
        issue_transaction_number = IssueTransactionNumber(test_repository)
        instance, status_code = issue_transaction_number.execute(
            "xxxxxx.xxxxxxx.xxxxxxxxxx")
        self.assertIsNone(instance)
        self.assertEqual(status_code, status.HTTP_200_OK)
