from django.test import SimpleTestCase
from rest_framework import status
from v1_card.buisiness_logic.get_card_balance.get_card_balance import \
    GetCardBalance
from v1_card.data.ICardBalanceRepository import ICardBalanceRepository
from v1_card.data.ICardDetailRepository import ICardDetailRepository
from v1_card.data.IMockCardBalanceRepository import IMockCardBalanceRepository
from v1_card.data.IMockCardDetailRepository import IMockCardDetailRepository

expected_access_token = 'header.payload.signature'


class GetCardDetailTests(SimpleTestCase):

    def test_card_101_success(self):
        '''
        正常
        '''

        test_detail_repository: ICardDetailRepository =\
            IMockCardDetailRepository()
        test_balance_reposiotry: ICardBalanceRepository =\
            IMockCardBalanceRepository()
        get_card_balance = GetCardBalance(
            test_detail_repository, test_balance_reposiotry)

        card_balance_instance, status_code = get_card_balance.execute(
            "9999999999990101", expected_access_token)

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNotNone(card_balance_instance)

        # 返却値チェック　フェーズ2で追記予定
        self.assertEqual(card_balance_instance.total_balance, 135_000)
        self.assertEqual(
            card_balance_instance.prepaid_value.total_balance, 30_000)
        self.assertEqual(
            card_balance_instance.payable_bonus.total_balance, 45_000)
        self.assertEqual(
            card_balance_instance.product_exchange_bonus.total_balance, 60_000)

    def test_card_102_failure(self):
        '''
        card.state=2, カードが利用停止状態
        '''

        test_detail_repository: ICardDetailRepository =\
            IMockCardDetailRepository()
        test_balance_reposiotry: ICardBalanceRepository =\
            IMockCardBalanceRepository()
        get_card_balance = GetCardBalance(
            test_detail_repository, test_balance_reposiotry)

        card_balance_instance, status_code = get_card_balance.execute(
            "9999999999990102", expected_access_token)

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNone(card_balance_instance)

    def test_card_103_failure(self):
        '''
        card.state=3, カードが破棄状態
        '''

        test_detail_repository: ICardDetailRepository =\
            IMockCardDetailRepository()
        test_balance_reposiotry: ICardBalanceRepository =\
            IMockCardBalanceRepository()
        get_card_balance = GetCardBalance(
            test_detail_repository, test_balance_reposiotry)

        card_balance_instance, status_code = get_card_balance.execute(
            "9999999999990103", expected_access_token)

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNone(card_balance_instance)

    def test_card_104_failure(self):
        '''
        card.provider_id='', 事業者が結びついていないカード
        '''

        test_detail_repository: ICardDetailRepository =\
            IMockCardDetailRepository()
        test_balance_reposiotry: ICardBalanceRepository =\
            IMockCardBalanceRepository()
        get_card_balance = GetCardBalance(
            test_detail_repository, test_balance_reposiotry)

        card_balance_instance, status_code = get_card_balance.execute(
            "9999999999990104", expected_access_token)

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNone(card_balance_instance)

    def test_card_101_wrong_access_token_failure(self):
        '''
        request_data['access_token'] != card_access_authorization.access_token
        request_bodyのaccess_tokenとカードアクセス認証情報のアクセストークン情報が一致しない。
        '''

        failure_access_token = 'xxxxxx.xxxxxxx.xxxxxxxxx'
        test_detail_repository: ICardDetailRepository =\
            IMockCardDetailRepository()
        test_balance_reposiotry: ICardBalanceRepository =\
            IMockCardBalanceRepository()
        get_card_balance = GetCardBalance(
            test_detail_repository, test_balance_reposiotry)

        card_balance_instance, status_code = get_card_balance.execute(
            "9999999999990101", failure_access_token)

        self.assertEqual(status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNone(card_balance_instance)

    def test_card_105_failure(self):
        '''
        card_access_authorization.access_token_state == 2, トークンステータスエラー
        '''

        test_detail_repository: ICardDetailRepository =\
            IMockCardDetailRepository()
        test_balance_reposiotry: ICardBalanceRepository =\
            IMockCardBalanceRepository()
        get_card_balance = GetCardBalance(
            test_detail_repository, test_balance_reposiotry)

        card_balance_instance, status_code = get_card_balance.execute(
            "9999999999990105", expected_access_token)

        self.assertEqual(status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNone(card_balance_instance)

    def test_card_106_failure(self):
        '''
        card.service_user_policy=False, サービス利用許可なし
        '''

        test_detail_repository: ICardDetailRepository =\
            IMockCardDetailRepository()
        test_balance_reposiotry: ICardBalanceRepository =\
            IMockCardBalanceRepository()
        get_card_balance = GetCardBalance(
            test_detail_repository, test_balance_reposiotry)

        card_balance_instance, status_code = get_card_balance.execute(
            "9999999999990106", expected_access_token)

        self.assertEqual(status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNone(card_balance_instance)

    def test_card_107_failure(self):
        '''
        card_access_authorization.expires_at < today(), トークン有効期限切れ
        '''

        test_detail_repository: ICardDetailRepository =\
            IMockCardDetailRepository()
        test_balance_reposiotry: ICardBalanceRepository =\
            IMockCardBalanceRepository()
        get_card_balance = GetCardBalance(
            test_detail_repository, test_balance_reposiotry)

        card_balance_instance, status_code = get_card_balance.execute(
            "9999999999990107", expected_access_token)

        self.assertEqual(status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNone(card_balance_instance)

    def test_wrong_card_no_failure(self):
        '''
        不正なcard_no
        '''
        test_detail_repository: ICardDetailRepository =\
            IMockCardDetailRepository()
        test_balance_reposiotry: ICardBalanceRepository =\
            IMockCardBalanceRepository()
        get_card_balance = GetCardBalance(
            test_detail_repository, test_balance_reposiotry)

        card_balance_instance, status_code = get_card_balance.execute(
            "999999999999XXXX", expected_access_token)

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNone(card_balance_instance)
