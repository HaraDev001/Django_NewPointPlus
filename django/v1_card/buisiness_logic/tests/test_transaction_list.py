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
from v1_card.buisiness_logic.transaction.transaction_list import TransactionList
from v1_card.serializers.transaction_serializers import TransactionResponseSerializer

from utils.datetime_utility import (now,
                                    to_utc_timestamp,
                                    get_datetime_hours_later_from
                                    )

class TransactionTests(SimpleTestCase):

    # フェーズ2でテスト項目を増やす
    def test_get_transaction_list_101_success(self):

        access_repository: IAccessTokenRepository = IMockAccessTokenRepository()

        issue_access_token = IssueAccessToken(access_repository)
        access_token_response, status_code = \
            issue_access_token.execute('9999999999990101', '0101')

        transaction_repository: ITransactionRepository = IMockTransactionRepository()
        test_repository = TransactionList(access_repository, transaction_repository)

        search = {
                    'transaction_type': 1,
                    'transaction_date': {
                        'transaction_start': '2021-07-01',
                        'transaction_end': '2021-07-30'
                    },
                    'transaction_status': 1
                }
        start_index = 0
        item_number = 2
        sort_order = 'asc'
        transaction_list, status_code = test_repository.execute('9999999999990101',
                                                                access_token_response.access_token,
                                                                search)
        response_list = []
        for transaction in transaction_list:
            responseserializer = TransactionResponseSerializer(transaction)
            response_list.append(responseserializer.data)

        response_list = test_repository.execute_sort(response_list, start_index,item_number, sort_order)

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertEqual(transaction_list[0].card_no, '9999999999990101')
        self.assertEqual(len(response_list), item_number)

    #条件指定なしの場合
    def test_get_transaction_list_102_success(self):

        access_repository: IAccessTokenRepository = IMockAccessTokenRepository()

        issue_access_token = IssueAccessToken(access_repository)
        access_token_response, status_code = \
            issue_access_token.execute('9999999999990101', '0101')

        transaction_repository: ITransactionRepository = IMockTransactionRepository()
        test_repository = TransactionList(access_repository, transaction_repository)

        sort_order = 'asc'
        search = {
                    'transaction_type': 1,
                    'transaction_date': {
                        'transaction_start': '2021-07-01',
                        'transaction_end': '2021-07-30'
                    },
                    'transaction_status': 1
                }
        transaction_list, status_code = test_repository.execute('9999999999990101',
                                                                access_token_response.access_token,
                                                                search)

        response_list = []
        for transaction in transaction_list:
            responseserializer = TransactionResponseSerializer(transaction)
            response_list.append(responseserializer.data)

        response_list = test_repository.execute_sort(response_list, None, None, None)

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertEqual(transaction_list[0].card_no, '9999999999990101')
        self.assertEqual(len(transaction_list), 3)


    #取得件数によってデータが0件
    def test_get_transaction_list_103_success(self):

        access_repository: IAccessTokenRepository = IMockAccessTokenRepository()

        issue_access_token = IssueAccessToken(access_repository)
        access_token_response, status_code = \
            issue_access_token.execute('9999999999990101', '0101')

        transaction_repository: ITransactionRepository = IMockTransactionRepository()
        test_repository = TransactionList(access_repository, transaction_repository)

        search = {
                    'transaction_type': 1,
                    'transaction_date': {
                        'transaction_start': '2021-07-01',
                        'transaction_end': '2021-07-30'
                    },
                    'transaction_status': 1
                }
        start_index = 0
        item_number = 1
        sort_order = 'asc'
        transaction_list, status_code = test_repository.execute('9999999999990101',
                                                                access_token_response.access_token,
                                                                search)
        response_list = []
        for transaction in transaction_list:
            responseserializer = TransactionResponseSerializer(transaction)
            response_list.append(responseserializer.data)

        response_list = test_repository.execute_sort(response_list, start_index,item_number, sort_order)

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertEqual(transaction_list[0].card_no, '9999999999990101')
        self.assertEqual(len(response_list), item_number)


    #開始位置によってデータが0件
    def test_get_transaction_list_104_success(self):

        access_repository: IAccessTokenRepository = IMockAccessTokenRepository()

        issue_access_token = IssueAccessToken(access_repository)
        access_token_response, status_code = \
            issue_access_token.execute('9999999999990101', '0101')

        transaction_repository: ITransactionRepository = IMockTransactionRepository()
        test_repository = TransactionList(access_repository, transaction_repository)

        search = {
                    'transaction_type': 1,
                    'transaction_date': {
                        'transaction_start': '2021-07-01',
                        'transaction_end': '2021-07-30'
                    },
                    'transaction_status': 1
                }
        start_index = 1
        item_number = 1
        sort_order = 'asc'
        transaction_list, status_code = test_repository.execute('9999999999990101',
                                                                access_token_response.access_token,
                                                                search)
        response_list = []
        for transaction in transaction_list:
            responseserializer = TransactionResponseSerializer(transaction)
            response_list.append(responseserializer.data)

        response_list = test_repository.execute_sort(response_list, start_index,item_number, sort_order)

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_list), 0)


    #日時絞り込みによってデータが0件
    def test_get_transaction_list_105_success(self):

        access_repository: IAccessTokenRepository = IMockAccessTokenRepository()

        issue_access_token = IssueAccessToken(access_repository)
        access_token_response, status_code = \
            issue_access_token.execute('9999999999990101', '0101')

        transaction_repository: ITransactionRepository = IMockTransactionRepository()
        test_repository = TransactionList(access_repository, transaction_repository)

        search = {
                    'transaction_type': 1,
                    'transaction_date': {
                        'transaction_start': '2021-06-01',
                        'transaction_end': '2021-06-30'
                    },
                    'transaction_status': 1
                }
        start_index = 1
        item_number = 1
        sort_order = 'asc'
        transaction_list, status_code = test_repository.execute('9999999999990101',
                                                                access_token_response.access_token,
                                                                search)
        response_list = []
        for transaction in transaction_list:
            responseserializer = TransactionResponseSerializer(transaction)
            response_list.append(responseserializer.data)

        response_list = test_repository.execute_sort(response_list, start_index,item_number, sort_order)

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_list), 0)


    #降順検索
    def test_get_transaction_list_106_success(self):

        access_repository: IAccessTokenRepository = IMockAccessTokenRepository()

        issue_access_token = IssueAccessToken(access_repository)
        access_token_response, status_code = \
            issue_access_token.execute('9999999999990101', '0101')

        transaction_repository: ITransactionRepository = IMockTransactionRepository()
        test_repository = TransactionList(access_repository, transaction_repository)

        search = {
                    'transaction_type': 1,
                    'transaction_date': {
                        'transaction_start': '2021-07-01',
                        'transaction_end': '2021-07-30'
                    },
                    'transaction_status': 1
                }
        start_index = 0
        item_number = 2
        sort_order = 'desc'
        transaction_list, status_code = test_repository.execute('9999999999990101',
                                                                access_token_response.access_token,
                                                                search)
        response_list = []
        for transaction in transaction_list:
            responseserializer = TransactionResponseSerializer(transaction)
            response_list.append(responseserializer.data)

        response_list = test_repository.execute_sort(response_list, start_index,item_number, sort_order)
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertEqual(transaction_list[0].transaction_number, '122345')
        self.assertEqual(len(response_list), item_number)


    #transaction_type指定の場合
    def test_get_transaction_list_107_success(self):

        access_repository: IAccessTokenRepository = IMockAccessTokenRepository()

        issue_access_token = IssueAccessToken(access_repository)
        access_token_response, status_code = \
            issue_access_token.execute('9999999999990101', '0101')

        transaction_repository: ITransactionRepository = IMockTransactionRepository()
        test_repository = TransactionList(access_repository, transaction_repository)

        sort_order = 'asc'
        search = {
                    'transaction_type': 2,
                    'transaction_date': {
                        'transaction_start': '2021-07-01',
                        'transaction_end': '2021-07-30'
                    },
                    'transaction_status': 1
                }
        transaction_list, status_code = test_repository.execute('9999999999990101',
                                                                access_token_response.access_token,
                                                                search)

        response_list = []
        for transaction in transaction_list:
            responseserializer = TransactionResponseSerializer(transaction)
            response_list.append(responseserializer.data)

        response_list = test_repository.execute_sort(response_list, None, None, None)

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertEqual(transaction_list[0].transaction_number, '122346')
        self.assertEqual(len(transaction_list), 1)


    #transaction_status指定の場合
    def test_get_transaction_list_108_success(self):

        access_repository: IAccessTokenRepository = IMockAccessTokenRepository()

        issue_access_token = IssueAccessToken(access_repository)
        access_token_response, status_code = \
            issue_access_token.execute('9999999999990101', '0101')

        transaction_repository: ITransactionRepository = IMockTransactionRepository()
        test_repository = TransactionList(access_repository, transaction_repository)

        sort_order = 'asc'
        search = {
                    'transaction_type': 2,
                    'transaction_date': {
                        'transaction_start': '2021-07-01',
                        'transaction_end': '2021-07-30'
                    },
                    'transaction_status': 2
                }
        transaction_list, status_code = test_repository.execute('9999999999990101',
                                                                access_token_response.access_token,
                                                                search)

        response_list = []
        for transaction in transaction_list:
            responseserializer = TransactionResponseSerializer(transaction)
            response_list.append(responseserializer.data)

        response_list = test_repository.execute_sort(response_list, None, None, None)

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertEqual(len(transaction_list), 0)