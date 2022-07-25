from rest_framework import status
from django.test import SimpleTestCase
from v1_terminal.data.IMockTransactionGetRepository import IMockTransactionGetRepository
from v1_terminal.data.ITransactionGetRepository import ITransactionGetRepository
from v1_terminal.buisiness_logic.transaction.get_transaction_detail import GetTransactionDetail


class GetTransactionDetailTests(SimpleTestCase):

    def test_get_transaction_detail_success(self):
        '''
        正常系
        '''

        test_repository: ITransactionGetRepository = IMockTransactionGetRepository()
        get_transaction_detail = GetTransactionDetail(test_repository)

        # リクエスト値設定
        terminal_access_token = 'header.payload.terminal_1'
        transaction_number = 1
        pk = 1

        response_data, response_status = get_transaction_detail.execute(
            terminal_access_token, transaction_number, pk
        )

        self.assertEqual(response_status, status.HTTP_200_OK)
        self.assertIsNotNone(response_data)
        self.assertEqual(response_data.transaction_number, 1)

    def test_get_transaction_detail_wrong_token_failure(self):
        '''
        トークン認証エラー
        '''

        test_repository: ITransactionGetRepository = IMockTransactionGetRepository()
        get_transaction_detail = GetTransactionDetail(test_repository)

        # リクエスト値設定
        terminal_access_token = 'header.payload.xxxxxxxxxx'
        transaction_number = 1
        pk = 1

        response_data, response_status = get_transaction_detail.execute(
            terminal_access_token, transaction_number, pk
        )

        self.assertEqual(response_status, status.HTTP_401_UNAUTHORIZED)
        self.assertIsNone(response_data)

    def test_get_transaction_detail_terminal_2_failure(self):
        '''
        current_unixtime > terminal_authorization.access_token_expires_at,
        トークン有効期限切れ
        '''
        test_repository: ITransactionGetRepository = IMockTransactionGetRepository()
        get_transaction_detail = GetTransactionDetail(test_repository)

        # リクエスト値設定
        terminal_access_token = 'header.payload.terminal_2'
        transaction_number = 1
        pk = 1

        response_data, response_status = get_transaction_detail.execute(
            terminal_access_token, transaction_number, pk
        )

        self.assertEqual(response_status, status.HTTP_401_UNAUTHORIZED)
        self.assertIsNone(response_data)

    def test_get_transaction_detail_card_102_failure(self):
        '''
        not card.service_user_policy,
        サービス利用許可なし
        '''
        test_repository: ITransactionGetRepository = IMockTransactionGetRepository()
        get_transaction_detail = GetTransactionDetail(test_repository)

        # リクエスト値設定
        terminal_access_token = 'header.payload.terminal_1'
        transaction_number = 2
        pk = 2

        response_data, response_status = get_transaction_detail.execute(
            terminal_access_token, transaction_number, pk
        )

        self.assertEqual(response_status, status.HTTP_403_FORBIDDEN)
        self.assertIsNone(response_data)

    def test_get_transaction_detail_mismatch_pk_and_transaction_number_failure(self):
        '''
        pk != transaction_number
        リクエスト内の取引番号とURIの取引番号の不一致
        '''
        test_repository: ITransactionGetRepository = IMockTransactionGetRepository()
        get_transaction_detail = GetTransactionDetail(test_repository)

        # リクエスト値設定
        terminal_access_token = 'header.payload.terminal_1'
        transaction_number = 1
        pk = 2

        response_data, response_status = get_transaction_detail.execute(
            terminal_access_token, transaction_number, pk
        )

        self.assertEqual(response_status, status.HTTP_400_BAD_REQUEST)
        self.assertIsNone(response_data)
