from unittest import mock
from rest_framework import status
from django.test import SimpleTestCase
from v1_card.buisiness_logic.access_token.issue_access_token \
    import IssueAccessToken
from v1_card.buisiness_logic.access_token.update_access_token \
    import UpdateAccessToken
from v1_card.data.IMockAccessTokenRepository import IMockAccessTokenRepository
from v1_card.data.ITransactionRepository import ITransactionRepository
from v1_card.data.IMockTransactionRepository import IMockTransactionRepository
from v1_card.buisiness_logic.transaction.transaction import Transaction

from utils.datetime_utility import (now,
                                    to_utc_timestamp,
                                    get_datetime_hours_later_from
                                    )

class TransactionTests(SimpleTestCase):

    # フェーズ2でテスト項目を増やす
    def test_get_transaction_101_success(self):

        access_repository: IAccessTokenRepository = IMockAccessTokenRepository()

        issue_access_token = IssueAccessToken(access_repository)
        access_token_response, status_code = \
            issue_access_token.execute('9999999999990101', '0101')

        transaction_repository: ITransactionRepository = IMockTransactionRepository()
        test_repository = Transaction(access_repository, transaction_repository)
        transaction, status_code = test_repository.execute('9999999999990101',
                                                                '122345', access_token_response.access_token)

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertEqual(transaction.card_no, '9999999999990101')
        self.assertIsNotNone(transaction)


