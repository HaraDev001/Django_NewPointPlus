from datetime import date
from unittest import mock

from .ICardDetailRepository import ICardDetailRepository


class IMockCardDetailRepository(ICardDetailRepository):
    '''
    ICardDetailRegistoryを実装したクラス

        ICardDetailRegistoryを実装したモックオブジェクトを扱うクラス

        Attributes:
            cards (dict): カード情報を保持
            card_configs(dict): カード設定情報を保持
            card_transactions(dict): カード取引履歴情報を保持
            card_access_authorizations(dict): カードアクセス認証情報を保持
    '''
    def __init__(self):

        self.cards = dict()
        self.card_configs = dict()
        self.card_transactions = dict()
        self.card_accrss_authorizations = dict()

        card_101 = mock.MagicMock(
            card_no='9999999999990101', card_pin='0101', state=1,
            payment=True, service_user_policy=True,
            provider_id='110000001', company_user_policy=True)
        card_102 = mock.MagicMock(
            card_no='9999999999990102', card_pin='0102', state=2,
            payment=True, service_user_policy=True,
            provider_id='110000001', company_user_policy=True)
        card_103 = mock.MagicMock(
            card_no='9999999999990103', card_pin='0103', state=3,
            payment=True, service_user_policy=True,
            provider_id='110000001', company_user_policy=False)
        card_104 = mock.MagicMock(
            card_no='9999999999990104', card_pin='0104', state=1,
            payment=True, service_user_policy=True,
            provider_id='', company_user_policy=False)
        card_105 = mock.MagicMock(
            card_no='9999999999990105', card_pin='0105', state=1,
            payment=False, service_user_policy=True,
            provider_id='110000001', company_user_policy=True)
        card_106 = mock.MagicMock(
            card_no='9999999999990106', card_pin='0106', state=1,
            payment=False, service_user_policy=False,
            provider_id='110000001', company_user_policy=True)
        card_107 = mock.MagicMock(
            card_no='9999999999990107', card_pin='0107', state=1,
            payment=False, service_user_policy=True,
            provider_id='110000001', company_user_policy=False)
        card_108 = mock.MagicMock(
            card_no='9999999999990108', card_pin='0108', state=1,
            payment=False,
            service_user_policy=False,
            provider_id='110000001', company_user_policy=False)

        for card in [
                card_101, card_102, card_103, card_104,
                card_105, card_106, card_107, card_108,
                ]:
            key = card.card_no
            self.cards[key] = card

        # カード設定情報
        card_config_101 = mock.MagicMock(
            card_no='9999999999990101',
            card_config_name='card_config_name',
            card_design='card_design',
            prepaid_value_unit='yen', payable_bonus_unit='yen',
            product_exchange_bonus_unit='yen',
            value_charge_limit_for_day=100000,
            value_charge_limit_for_month=1000000,
            value_payment_limit_for_day=100000,
            value_payment_limit_for_month=1000000)
        card_config_102 = mock.MagicMock(
            card_no='9999999999990102',
            card_config_name='card_config_name',
            card_design='card_design',
            prepaid_value_unit='yen', payable_bonus_unit='yen',
            product_exchange_bonus_unit='yen',
            value_charge_limit_for_day=100000,
            value_charge_limit_for_month=1000000,
            value_payment_limit_for_day=100000,
            value_payment_limit_for_month=1000000)
        card_config_103 = mock.MagicMock(
            card_no='9999999999990103',
            card_config_name='card_config_name',
            card_design='card_design',
            prepaid_value_unit='yen', payable_bonus_unit='yen',
            product_exchange_bonus_unit='yen',
            value_charge_limit_for_day=100000,
            value_charge_limit_for_month=1000000,
            value_payment_limit_for_day=100000,
            value_payment_limit_for_month=1000000)
        card_config_104 = mock.MagicMock(
            card_no='9999999999990104',
            card_config_name='card_config_name',
            card_design='card_design',
            prepaid_value_unit='yen', payable_bonus_unit='yen',
            product_exchange_bonus_unit='yen',
            value_charge_limit_for_day=100000,
            value_charge_limit_for_month=1000000,
            value_payment_limit_for_day=100000,
            value_payment_limit_for_month=1000000)
        card_config_105 = mock.MagicMock(
            card_no='9999999999990105',
            card_config_name='card_config_name',
            card_design='card_design',
            prepaid_value_unit='yen', payable_bonus_unit='yen',
            product_exchange_bonus_unit='yen',
            value_charge_limit_for_day=100000,
            value_charge_limit_for_month=1000000,
            value_payment_limit_for_day=100000,
            value_payment_limit_for_month=1000000)
        card_config_106 = mock.MagicMock(
            card_no='9999999999990106',
            card_config_name='card_config_name',
            card_design='card_design',
            prepaid_value_unit='yen', payable_bonus_unit='yen',
            product_exchange_bonus_unit='yen',
            value_charge_limit_for_day=100000,
            value_charge_limit_for_month=1000000,
            value_payment_limit_for_day=100000,
            value_payment_limit_for_month=1000000)
        card_config_107 = mock.MagicMock(
            card_no='9999999999990107',
            card_config_name='card_config_name',
            card_design='card_design',
            prepaid_value_unit='yen', payable_bonus_unit='yen',
            product_exchange_bonus_unit='yen',
            value_charge_limit_for_day=100000,
            value_charge_limit_for_month=1000000,
            value_payment_limit_for_day=100000,
            value_payment_limit_for_month=1000000)
        card_config_108 = mock.MagicMock(
            card_no='9999999999990108',
            card_config_name='card_config_name',
            card_design='card_design',
            prepaid_value_unit='yen', payable_bonus_unit='yen',
            product_exchange_bonus_unit='yen',
            value_charge_limit_for_day=100000,
            value_charge_limit_for_month=1000000,
            value_payment_limit_for_day=100000,
            value_payment_limit_for_month=1000000)

        for card_config in [
                card_config_101, card_config_102, card_config_103,
                card_config_104, card_config_105, card_config_106,
                card_config_107, card_config_108
                ]:
            key = card_config.card_no
            self.card_configs[key] = card_config

        # カード取引履歴情報
        card_transaction_101 = mock.MagicMock(
            card_no='9999999999990101',
            value_charge_result_for_day=1000,
            value_charge_result_for_month=30000,
            value_payment_result_for_day=10000,
            value_payment_result_for_month=20000)
        card_transaction_102 = mock.MagicMock(
            card_no='9999999999990102',
            value_charge_result_for_day=1000,
            value_charge_result_for_month=30000,
            value_payment_result_for_day=10000,
            value_payment_result_for_month=20000)
        card_transaction_103 = mock.MagicMock(
            card_no='9999999999990103',
            value_charge_result_for_day=1000,
            value_charge_result_for_month=30000,
            value_payment_result_for_day=10000,
            value_payment_result_for_month=20000)
        card_transaction_104 = mock.MagicMock(
            card_no='9999999999990104',
            value_charge_result_for_day=1000,
            value_charge_result_for_month=30000,
            value_payment_result_for_day=10000,
            value_payment_result_for_month=20000)
        card_transaction_105 = mock.MagicMock(
            card_no='9999999999990105',
            value_charge_result_for_day=1000,
            value_charge_result_for_month=30000,
            value_payment_result_for_day=10000,
            value_payment_result_for_month=20000)
        card_transaction_106 = mock.MagicMock(
            card_no='9999999999990106',
            value_charge_result_for_day=1000,
            value_charge_result_for_month=30000,
            value_payment_result_for_day=10000,
            value_payment_result_for_month=20000)
        card_transaction_107 = mock.MagicMock(
            card_no='9999999999990107',
            value_charge_result_for_day=1000,
            value_charge_result_for_month=30000,
            value_payment_result_for_day=10000,
            value_payment_result_for_month=20000)
        card_transaction_108 = mock.MagicMock(
            card_no='9999999999990108',
            value_charge_result_for_day=1000,
            value_charge_result_for_month=30000,
            value_payment_result_for_day=10000,
            value_payment_result_for_month=20000)

        for card_transaction in [
                card_transaction_101, card_transaction_102,
                card_transaction_103, card_transaction_104,
                card_transaction_105, card_transaction_106,
                card_transaction_107, card_transaction_108
                ]:
            key = card_transaction.card_no
            self.card_transactions[key] = card_transaction

        # カードアクセス認証情報
        card_accrss_authorization_101 = mock.MagicMock(
            card_no='9999999999990101',
            access_token_state=1,
            expires_at=date(2025, 7, 31),
            access_token='header.payload.signature')
        card_accrss_authorization_102 = mock.MagicMock(
            card_no='9999999999990102',
            access_token_state=1,
            expires_at=date(2025, 7, 31),
            access_token='header.payload.signature')
        card_accrss_authorization_103 = mock.MagicMock(
            card_no='9999999999990103',
            access_token_state=1,
            expires_at=date(2025, 7, 31),
            access_token='header.payload.signature')
        card_accrss_authorization_104 = mock.MagicMock(
            card_no='9999999999990104',
            access_token_state=1,
            expires_at=date(2025, 7, 31),
            access_token='header.payload.signature')
        card_accrss_authorization_105 = mock.MagicMock(
            card_no='9999999999990105',
            access_token_state=2,
            expires_at=date(2025, 7, 31),
            access_token='header.payload.signature')
        card_accrss_authorization_106 = mock.MagicMock(
            card_no='9999999999990106',
            access_token_state=1,
            expires_at=date(2025, 7, 31),
            access_token='header.payload.signature')
        card_accrss_authorization_107 = mock.MagicMock(
            card_no='9999999999990107',
            access_token_state=1,
            expires_at=date(2021, 7, 1),
            access_token='header.payload.signature')
        card_accrss_authorization_108 = mock.MagicMock(
            card_no='9999999999990108',
            access_token_state=1,
            expires_at=date(2025, 7, 31),
            access_token='header.payload.signature')

        for card_accrss_authorization in [
                card_accrss_authorization_101, card_accrss_authorization_102,
                card_accrss_authorization_103, card_accrss_authorization_104,
                card_accrss_authorization_105, card_accrss_authorization_106,
                card_accrss_authorization_107, card_accrss_authorization_108
                ]:
            key = card_accrss_authorization.card_no
            self.card_accrss_authorizations[key] = card_accrss_authorization

    def get_card_by_no(self, card_no):
        '''カード情報を取得する.

            カード情報を取得する.

        Args:
            card_no (str型): カード番号.

        Returns:
            カード情報: 指定されたカード番号のモックオブジェクトがなければ、例外を発生させる.

        Raises:
            Exception: リクエストされたカード番号＆PINで一致するカードがない

        '''

        key = card_no
        try:
            card = self.cards[key]
        except KeyError:
            raise Exception('リクエストされたカード番号で一致するカードがない')
        return card

    def get_card_config_by_no(self, card_no):
        '''カード設定情報を取得する.

            カード設定情報を取得する.

        Args:
            card_no (str型): カード番号.

        Returns:
            カード設定情報: 指定されたカード番号のモックオブジェクトがなければ、例外を発生させる.

        Raises:
            Exception: リクエストされたカード番号＆PINで一致するカードがない

        '''
        key = card_no
        try:
            card_config = self.card_configs[key]
        except KeyError:
            raise Exception('リクエストされたカード番号で一致するカードがない')
        return card_config

    def get_card_access_authorization_by_no(self, card_no):
        '''カードアクセス認証情報を取得する.

            カード設定情報を取得する.

        Args:
            card_no (str型): カード番号.

        Returns:
            カードアクセス認証情報: 指定されたカード番号のモックオブジェクトがなければ、例外を発生させる.

        Raises:
            Exception: リクエストされたカード番号＆PINで一致するカードがない

        '''
        key = card_no
        try:
            card_accrss_authorization = self.card_accrss_authorizations[key]
        except KeyError:
            raise Exception('リクエストされたカード番号で一致するカードがない')
        return card_accrss_authorization

    def get_card_transaction_by_no(self, card_no):
        '''カード取引履歴情報を取得する.

            カード取引履歴情報を取得する.

        Args:
            card_no (str型): カード番号.

        Returns:
            カード取引履歴情報: 指定されたカード番号のモックオブジェクトがなければ、例外を発生させる.

        Raises:
            Exception: リクエストされたカード番号＆PINで一致するカードがない

        '''
        key = card_no
        try:
            card_transaction = self.card_transactions[key]
        except KeyError:
            raise Exception('リクエストされたカード番号で一致するカードがない')
        return card_transaction
