from django.test import SimpleTestCase
from rest_framework import status
from v1_terminal.buisiness_logic.card.get_card_balance import GetCardBalance
from v1_terminal.data.ICardBalanceRepository import ICardBalanceRepository
from v1_terminal.data.ICardDetailRepository import ICardDetailRepository
from v1_terminal.data.IMockCardBalanceRepository import \
    IMockCardBalanceRepository
from v1_terminal.data.IMockCardDetailRepository import \
    IMockCardDetailRepository


class GetCardDetailTests(SimpleTestCase):

    def test_card_101_success(self):
        '''
        正常系
        '''

        test_detail_repository: ICardDetailRepository =\
            IMockCardDetailRepository()
        test_balance_reposiotry: ICardBalanceRepository =\
            IMockCardBalanceRepository()
        get_card_balance = GetCardBalance(
            test_detail_repository, test_balance_reposiotry)

        card_balance_instance, status_code = get_card_balance.execute(
            '9999999999990101', '9999999999990101',
            '0101', 'header.payload.terminal_1')

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
        card.state=2, サービス利用許可なし
        '''

        test_detail_repository: ICardDetailRepository =\
            IMockCardDetailRepository()
        test_balance_reposiotry: ICardBalanceRepository =\
            IMockCardBalanceRepository()
        get_card_balance = GetCardBalance(
            test_detail_repository, test_balance_reposiotry)

        card_balance_instance, status_code = get_card_balance.execute(
            '9999999999990102', '9999999999990102',
            '0102', 'header.payload.terminal_1')

        self.assertEqual(status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNone(card_balance_instance)

    def test_card_104_failure(self):
        '''
        provider_id='', 事業者が結びついていないカード
        '''

        test_detail_repository: ICardDetailRepository =\
            IMockCardDetailRepository()
        test_balance_reposiotry: ICardBalanceRepository =\
            IMockCardBalanceRepository()
        get_card_balance = GetCardBalance(
            test_detail_repository, test_balance_reposiotry)

        card_balance_instance, status_code = get_card_balance.execute(
            '9999999999990104', '9999999999990104',
            '0104', 'header.payload.terminal_1')

        self.assertEqual(status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNone(card_balance_instance)

    def test_access_token_2_failure(self):
        '''
        current_unixtime > terminal_authorization.access_token_expires_at,
        トークン有効期限切れ
        '''

        test_detail_repository: ICardDetailRepository =\
            IMockCardDetailRepository()
        test_balance_reposiotry: ICardBalanceRepository =\
            IMockCardBalanceRepository()
        get_card_balance = GetCardBalance(
            test_detail_repository, test_balance_reposiotry)

        card_balance_instance, status_code = get_card_balance.execute(
            '9999999999990101', '9999999999990101',
            '0101', "header.payload.terminal_2")

        self.assertEqual(status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNone(card_balance_instance)

    def test_mismatch_pk_and_card_no_failure(self):
        '''
        pk != card_no
        URIのカード番号とreuqest内のカード番号の不一致
        '''

        test_detail_repository: ICardDetailRepository =\
            IMockCardDetailRepository()
        test_balance_reposiotry: ICardBalanceRepository =\
            IMockCardBalanceRepository()
        get_card_balance = GetCardBalance(
            test_detail_repository, test_balance_reposiotry)

        card_balance_instance, status_code = get_card_balance.execute(
            '9999999999990101', '9999999999990102',
            '0101', "header.payload.terminal_1")

        self.assertEqual(status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNone(card_balance_instance)

    def test_wrong_access_token_failure(self):
        '''
        認証トークンが店舗端末認証情報のレコードと不一致
        '''

        test_detail_repository: ICardDetailRepository =\
            IMockCardDetailRepository()
        test_balance_reposiotry: ICardBalanceRepository =\
            IMockCardBalanceRepository()
        get_card_balance = GetCardBalance(
            test_detail_repository, test_balance_reposiotry)

        card_balance_instance, status_code = get_card_balance.execute(
            '9999999999990101', '9999999999990101',
            '0101', "xxxxxx.xxxxxxx.xxxxxxxxxx")

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNone(card_balance_instance)

    def test_wrong_card_no_failure(self):
        '''
        存在しないカード番号
        '''

        test_detail_repository: ICardDetailRepository =\
            IMockCardDetailRepository()
        test_balance_reposiotry: ICardBalanceRepository =\
            IMockCardBalanceRepository()
        get_card_balance = GetCardBalance(
            test_detail_repository, test_balance_reposiotry)

        card_balance_instance, status_code = get_card_balance.execute(
            '999999999999xxxx', '999999999999xxxx',
            '0101', 'header.payload.terminal_1')

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNone(card_balance_instance)

    def test_wrong_card_pin_failure(self):
        '''
        カード番号とPINの不一致
        '''

        test_detail_repository: ICardDetailRepository =\
            IMockCardDetailRepository()
        test_balance_reposiotry: ICardBalanceRepository =\
            IMockCardBalanceRepository()
        get_card_balance = GetCardBalance(
            test_detail_repository, test_balance_reposiotry)

        card_balance_instance, status_code = get_card_balance.execute(
            '9999999999990101', '9999999999990101',
            'xxxx', 'header.payload.terminal_1')

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNone(card_balance_instance)
