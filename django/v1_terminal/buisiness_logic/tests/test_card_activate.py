from django.test import SimpleTestCase
from rest_framework import status
from v1_terminal.buisiness_logic.card.card_activate import ActivateCard
from v1_terminal.data.ICardActivateRepository import ICardActivateRepository
from v1_terminal.data.IMockCardActivateRepository import \
    IMockCardActivateRepository


class CardActivateTests(SimpleTestCase):

    def test_card_101_success(self):

        test_repository: ICardActivateRepository =\
            IMockCardActivateRepository()
        card_activate = ActivateCard(test_repository)
        card = test_repository.identify_card('9999999999990101', '0101')
        # カードは未アクティベート状態
        self.assertEqual(card.state, 0)
        status_code = card_activate.execute(
            '9999999999990101', '9999999999990101',
            '0101', 'header.payload.terminal_1')
        self.assertEqual(status_code, status.HTTP_200_OK)
        # カードはアクティベート状態
        self.assertEqual(card.state, 1)

    def test_card_102_failure(self):
        '''
        card.service_user_policy=False, サービス利用許可なし
        '''

        test_repository: ICardActivateRepository =\
            IMockCardActivateRepository()
        card_activate = ActivateCard(test_repository)
        status_code = card_activate.execute(
            '9999999999990102', '9999999999990102',
            '0102', 'header.payload.terminal_1')
        self.assertEqual(status_code, status.HTTP_400_BAD_REQUEST)

    def test_card_103_failure(self):
        '''
        card.state != 0, 未アクティベートでないカード
        '''
        test_repository: ICardActivateRepository =\
            IMockCardActivateRepository()
        card_activate = ActivateCard(test_repository)
        status_code = card_activate.execute(
            '9999999999990103', '9999999999990103',
            '0103', 'header.payload.terminal_1')
        self.assertEqual(status_code, status.HTTP_400_BAD_REQUEST)

    def test_terminal_2_failure(self):
        '''
        current_unixtime > terminal_authorization.access_token_expires_at,
        トークン有効期限切れ
        '''

        test_repository: ICardActivateRepository =\
            IMockCardActivateRepository()
        card_activate = ActivateCard(test_repository)
        status_code = card_activate.execute(
            '9999999999990101', '9999999999990101',
            '0101', 'header.payload.terminal_2')
        self.assertEqual(status_code, status.HTTP_400_BAD_REQUEST)

    def test_mismatch_pk_and_card_no_failure(self):
        '''
        pk != card_no
        URIのカード番号とreuqest内のカード番号の不一致
        '''
        test_repository: ICardActivateRepository =\
            IMockCardActivateRepository()
        card_activate = ActivateCard(test_repository)
        status_code = card_activate.execute(
            '9999999999990101', '9999999999990102',
            '0101', 'header.payload.terminal_1')
        self.assertEqual(status_code, status.HTTP_400_BAD_REQUEST)

    def test_wrong_card_no_failure(self):
        '''
        存在しないカード番号
        '''
        test_repository: ICardActivateRepository =\
            IMockCardActivateRepository()
        card_activate = ActivateCard(test_repository)
        status_code = card_activate.execute(
            '999999999999xxxx', '999999999999xxxx',
            '0101', 'header.payload.terminal_1')
        self.assertEqual(status_code, status.HTTP_200_OK)

    def test_wrong_card_pin_failure(self):
        '''
        カード番号とPINの不一致
        '''
        test_repository: ICardActivateRepository =\
            IMockCardActivateRepository()
        card_activate = ActivateCard(test_repository)
        status_code = card_activate.execute(
            '9999999999990101', '9999999999990101',
            'xxxx', 'header.payload.terminal_1')
        self.assertEqual(status_code, status.HTTP_200_OK)

    def test_wrong_access_token_failure(self):
        '''
        認証トークンが店舗端末認証情報のレコードと不一致
        '''
        test_repository: ICardActivateRepository =\
            IMockCardActivateRepository()
        card_activate = ActivateCard(test_repository)
        status_code = card_activate.execute(
            '9999999999990101', '9999999999990101',
            '0101', 'xxxxxx.xxxxxxx.xxxxxxxxx')
        self.assertEqual(status_code, status.HTTP_200_OK)
