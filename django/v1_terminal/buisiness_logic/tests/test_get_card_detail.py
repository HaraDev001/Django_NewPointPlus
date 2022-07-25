from django.test import SimpleTestCase
from rest_framework import status
from v1_terminal.buisiness_logic.card.get_card_detail import GetCardDetail
from v1_terminal.data.ICardDetailRepository import ICardDetailRepository
from v1_terminal.data.IMockCardDetailRepository import \
    IMockCardDetailRepository


class GetCardDetailTests(SimpleTestCase):

    def test_card_101_success(self):
        '''
        正常系
        '''
        test_repository: ICardDetailRepository =\
            IMockCardDetailRepository()
        get_card_detail = GetCardDetail(test_repository)
        instance, status_code = get_card_detail.execute(
            '9999999999990101', '9999999999990101',
            '0101', 'header.payload.terminal_1')
        self.assertIsNotNone(instance)
        self.assertEqual(status_code, status.HTTP_200_OK)

        # 値チェック
        self.assertEqual(instance.card_no, '9999999999990101')

    def test_card_102_failure(self):
        '''
        card.service_user_policy=False, サービス利用許可なし
        '''

        test_repository: ICardDetailRepository =\
            IMockCardDetailRepository()
        card_activate = GetCardDetail(test_repository)
        instance, status_code = card_activate.execute(
            '9999999999990102', '9999999999990102',
            '0102', 'header.payload.terminal_1')
        self.assertIsNone(instance)
        self.assertEqual(status_code, status.HTTP_400_BAD_REQUEST)

    def test_card_104_failure(self):
        '''
        provider_id='', 事業者が結びついていないカード
        '''
        test_repository: ICardDetailRepository =\
            IMockCardDetailRepository()
        card_activate = GetCardDetail(test_repository)
        instance, status_code = card_activate.execute(
            '9999999999990104', '9999999999990104',
            '0104', 'header.payload.terminal_1')
        self.assertIsNone(instance)
        self.assertEqual(status_code, status.HTTP_400_BAD_REQUEST)

    def test_access_token_2_failure(self):
        '''
        current_unixtime > terminal_authorization.access_token_expires_at,
        トークン有効期限切れ
        '''

        test_repository: ICardDetailRepository =\
            IMockCardDetailRepository()
        get_card_detail = GetCardDetail(test_repository)
        instance, status_code = get_card_detail.execute(
            '9999999999990101', '9999999999990101',
            '0101', "header.payload.terminal_2")
        self.assertIsNone(instance)
        self.assertEqual(status_code, status.HTTP_400_BAD_REQUEST)

    def test_mismatch_pk_and_card_no_failure(self):
        '''
        pk != card_no
        URIのカード番号とreuqest内のカード番号の不一致
        '''
        test_repository: ICardDetailRepository =\
            IMockCardDetailRepository()
        card_activate = GetCardDetail(test_repository)
        instance, status_code = card_activate.execute(
            '9999999999990101', '9999999999990102',
            '0101', 'header.payload.terminal_1')
        self.assertIsNone(instance)
        self.assertEqual(status_code, status.HTTP_400_BAD_REQUEST)

    def test_wrong_access_token_failure(self):
        '''
        認証トークンが店舗端末認証情報のレコードと不一致
        '''

        test_repository: ICardDetailRepository =\
            IMockCardDetailRepository()
        get_card_detail = GetCardDetail(test_repository)
        instance, status_code = get_card_detail.execute(
            '9999999999990101', '9999999999990101',
            '0101', "xxxxxx.xxxxxxx.xxxxxxxxxx")
        self.assertIsNone(instance)
        self.assertEqual(status_code, status.HTTP_200_OK)

    def test_wrong_card_no_failure(self):
        '''
        存在しないカード番号
        '''
        test_repository: ICardDetailRepository =\
            IMockCardDetailRepository()
        card_activate = GetCardDetail(test_repository)
        instance, status_code = card_activate.execute(
            '999999999999xxxx', '999999999999xxxx',
            '0101', 'header.payload.terminal_1')
        self.assertIsNone(instance)
        self.assertEqual(status_code, status.HTTP_200_OK)

    def test_wrong_card_pin_failure(self):
        '''
        カード番号とPINの不一致
        '''
        test_repository: ICardDetailRepository =\
            IMockCardDetailRepository()
        card_activate = GetCardDetail(test_repository)
        instance, status_code = card_activate.execute(
            '9999999999990101', '9999999999990101',
            'xxxx', 'header.payload.terminal_1')
        self.assertIsNone(instance)
        self.assertEqual(status_code, status.HTTP_200_OK)
