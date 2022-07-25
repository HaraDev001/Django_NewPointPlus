from rest_framework import status
from django.test import SimpleTestCase
from v1_terminal.data.IMockTransactionGetRepository import IMockTransactionGetRepository
from v1_terminal.data.ITransactionGetRepository import ITransactionGetRepository
from v1_terminal.buisiness_logic.transaction.get_transaction_list import GetTransactionList
from utils.datetime_utility import get_datetime


class TrabsactionListTests(SimpleTestCase):
    # フェーズ2以降正常系のテストケースを補完する。
    def test_get_transaction_list_success(self):
        '''
        正常系　全件
        出力は6件
        '''

        test_repository: ITransactionGetRepository = IMockTransactionGetRepository()
        get_transaction_list = GetTransactionList(test_repository)

        # リクエスト値設定
        start_index = 0
        item_number = 6
        terminal_access_token = 'header.payload.terminal_1'
        transaction_type = None
        transaction_start = None
        transaction_end = None
        transaction_status = None
        terminal_no = None
        card_no = None
        magnetic_information = None
        sort_order = None

        transaction_list, response_status = get_transaction_list.execute(
            terminal_access_token, transaction_type, transaction_start, transaction_end, transaction_status,
            terminal_no, card_no, magnetic_information
        )
        response_data = get_transaction_list.execute_sort(
            transaction_list, start_index, item_number, sort_order)

        self.assertEqual(response_status, status.HTTP_200_OK)
        # 降順で並び替えられている
        self.assertTrue(
            response_data.transaction_history[0].transaction_at >= response_data.transaction_history[1].transaction_at)
        self.assertEqual(len(response_data.transaction_history), item_number)

    def test_get_transaction_list_asc_success(self):
        '''
        正常系　全件 昇順
        出力は6件
        '''

        test_repository: ITransactionGetRepository = IMockTransactionGetRepository()
        get_transaction_list = GetTransactionList(test_repository)

        # リクエスト値設定
        start_index = 0
        item_number = 6
        terminal_access_token = 'header.payload.terminal_1'
        transaction_type = None
        transaction_start = None
        transaction_end = None
        transaction_status = None
        terminal_no = None
        card_no = None
        magnetic_information = None
        sort_order = 'asc'

        transaction_list, response_status = get_transaction_list.execute(
            terminal_access_token, transaction_type, transaction_start, transaction_end, transaction_status,
            terminal_no, card_no, magnetic_information
        )
        response_data = get_transaction_list.execute_sort(
            transaction_list, start_index, item_number, sort_order)

        self.assertEqual(response_status, status.HTTP_200_OK)
        # 昇順で並び替えられている
        self.assertTrue(
            response_data.transaction_history[0].transaction_at <= response_data.transaction_history[1].transaction_at
        )
        self.assertEqual(len(response_data.transaction_history), item_number)

    def test_get_transaction_list_item_number_1_success(self):
        '''
        正常系　item_number=1
        出力は1件
        '''

        test_repository: ITransactionGetRepository = IMockTransactionGetRepository()
        get_transaction_list = GetTransactionList(test_repository)

        # リクエスト値設定
        start_index = 0
        item_number = 1
        terminal_access_token = 'header.payload.terminal_1'
        transaction_type = None
        transaction_start = None
        transaction_end = None
        transaction_status = None
        terminal_no = None
        card_no = None
        magnetic_information = None
        sort_order = None

        transaction_list, response_status = get_transaction_list.execute(
            terminal_access_token, transaction_type, transaction_start, transaction_end, transaction_status,
            terminal_no, card_no, magnetic_information
        )
        response_data = get_transaction_list.execute_sort(
            transaction_list, start_index, item_number, sort_order)

        self.assertEqual(response_status, status.HTTP_200_OK)
        self.assertEqual(len(response_data.transaction_history), item_number)

    def test_get_transaction_list_item_number_0_success(self):
        '''
        正常系　item_number=0
        出力は0件
        '''

        test_repository: ITransactionGetRepository = IMockTransactionGetRepository()
        get_transaction_list = GetTransactionList(test_repository)

        # リクエスト値設定
        start_index = 0
        item_number = 0
        terminal_access_token = 'header.payload.terminal_1'
        transaction_type = None
        transaction_start = None
        transaction_end = None
        transaction_status = None
        terminal_no = None
        card_no = None
        magnetic_information = None
        sort_order = None

        transaction_list, response_status = get_transaction_list.execute(
            terminal_access_token, transaction_type, transaction_start, transaction_end, transaction_status,
            terminal_no, card_no, magnetic_information
        )
        response_data = get_transaction_list.execute_sort(
            transaction_list, start_index, item_number, sort_order)

        self.assertEqual(response_status, status.HTTP_200_OK)
        self.assertEqual(len(response_data.transaction_history), item_number)
        self.assertEqual(response_data.transaction_history, [])

    def test_get_transaction_list_start_index_3_success(self):
        '''
        正常系　start_index=3
        出力は3件
        '''

        test_repository: ITransactionGetRepository = IMockTransactionGetRepository()
        get_transaction_list = GetTransactionList(test_repository)

        # リクエスト値設定
        start_index = 3
        item_number = 6
        terminal_access_token = 'header.payload.terminal_1'
        transaction_type = None
        transaction_start = None
        transaction_end = None
        transaction_status = None
        terminal_no = None
        card_no = None
        magnetic_information = None
        sort_order = None

        transaction_list, response_status = get_transaction_list.execute(
            terminal_access_token, transaction_type, transaction_start, transaction_end, transaction_status,
            terminal_no, card_no, magnetic_information
        )
        response_data = get_transaction_list.execute_sort(
            transaction_list, start_index, item_number, sort_order)

        self.assertEqual(response_status, status.HTTP_200_OK)
        # 降順で並び替えられている
        self.assertTrue(
            response_data.transaction_history[0].transaction_at >= response_data.transaction_history[1].transaction_at)
        self.assertEqual(len(response_data.transaction_history), 3)

    def test_get_transaction_list_wrong_card_failure(self):
        """
        カード番号に一致するカードがない
        """

        test_repository: ITransactionGetRepository = IMockTransactionGetRepository()
        get_transaction_list = GetTransactionList(test_repository)

        # リクエスト値設定
        terminal_access_token = 'header.payload.terminal_1'
        transaction_type = None
        transaction_start = None
        transaction_end = None
        transaction_status = None
        terminal_no = None
        card_no = "999999999999xxxxx"
        magnetic_information = None

        transaction_list, response_status = get_transaction_list.execute(
            terminal_access_token, transaction_type, transaction_start, transaction_end, transaction_status,
            terminal_no, card_no, magnetic_information
        )

        self.assertEqual(response_status, status.HTTP_200_OK)
        self.assertIsNone(transaction_list)

    def test_get_transaction_list_card_102_failure(self):
        """
        not card.service_user_policy,
        サービス利用許可なし
        """

        test_repository: ITransactionGetRepository = IMockTransactionGetRepository()
        get_transaction_list = GetTransactionList(test_repository)

        # リクエスト値設定
        terminal_access_token = 'header.payload.terminal_1'
        transaction_type = None
        transaction_start = None
        transaction_end = None
        transaction_status = None
        terminal_no = None
        card_no = "9999999999990102"
        magnetic_information = None

        transaction_list, response_status = get_transaction_list.execute(
            terminal_access_token, transaction_type, transaction_start, transaction_end, transaction_status,
            terminal_no, card_no, magnetic_information
        )

        self.assertEqual(response_status, status.HTTP_403_FORBIDDEN)
        self.assertIsNone(transaction_list)

    def test_get_transaction_list_wrong_access_token_failure(self):
        """
        トークン認証エラー
        """

        test_repository: ITransactionGetRepository = IMockTransactionGetRepository()
        get_transaction_list = GetTransactionList(test_repository)

        # リクエスト値設定
        terminal_access_token = 'header.payload.terminal_x'
        transaction_type = None
        transaction_start = None
        transaction_end = None
        transaction_status = None
        terminal_no = None
        card_no = None
        magnetic_information = None

        transaction_list, response_status = get_transaction_list.execute(
            terminal_access_token, transaction_type, transaction_start, transaction_end, transaction_status,
            terminal_no, card_no, magnetic_information
        )

        self.assertEqual(response_status, status.HTTP_401_UNAUTHORIZED)
        self.assertIsNone(transaction_list)

    def test_get_transaction_list_terminal_2_failure(self):
        """
        current_unixtime > terminal_authorization.access_token_expires_at,
        トークン有効期限切れ
        """

        test_repository: ITransactionGetRepository = IMockTransactionGetRepository()
        get_transaction_list = GetTransactionList(test_repository)

        # リクエスト値設定
        terminal_access_token = 'header.payload.terminal_2'
        transaction_type = None
        transaction_start = None
        transaction_end = None
        transaction_status = None
        terminal_no = None
        card_no = None
        magnetic_information = None

        transaction_list, response_status = get_transaction_list.execute(
            terminal_access_token, transaction_type, transaction_start, transaction_end, transaction_status,
            terminal_no, card_no, magnetic_information
        )

        self.assertEqual(response_status, status.HTTP_401_UNAUTHORIZED)
        self.assertIsNone(transaction_list)

    def test_get_transaction_wrong_aggregation_date(self):
        """
        transaction_start and transaction_end,
        取引日時の終了日時が開始日時よりも前の日時

        """

        test_repository: ITransactionGetRepository = IMockTransactionGetRepository()
        get_transaction_list = GetTransactionList(test_repository)

        # リクエスト値設定
        terminal_access_token = 'header.payload.terminal_2'
        transaction_type = None
        transaction_start = get_datetime(2021, 7, 31)
        transaction_end = get_datetime(2021, 7, 1)
        transaction_status = None
        terminal_no = None
        card_no = None
        magnetic_information = None

        transaction_list, response_status = get_transaction_list.execute(
            terminal_access_token, transaction_type, transaction_start, transaction_end, transaction_status,
            terminal_no, card_no, magnetic_information
        )

        self.assertEqual(response_status, status.HTTP_400_BAD_REQUEST)
        self.assertIsNone(transaction_list)
