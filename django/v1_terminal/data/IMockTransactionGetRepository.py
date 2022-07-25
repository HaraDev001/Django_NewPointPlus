from datetime import datetime, timedelta, timezone
from unittest import mock

from utils.datetime_utility import to_utc_timestamp

from .ITransactionGetRepository import ITransactionGetRepository


class IMockTransactionGetRepository(ITransactionGetRepository):
    '''
    ITransactionGetRespositoryを実装したクラス

        ITransactionGetRepositoryを実装したモックオブジェクトを扱うクラス

        Attributes:
            transactions_for_detail (dict): 取引履歴詳細取得のための取引履歴情報を保持
            transactions_for_list (dict): 取引履歴一覧取得のための取引履歴情報を保持
            terminal_authorizations (dict): 店舗端末認証情報を保持
            cards (dict): カード情報を保持
    '''
    def __init__(self):
        self.transactions_for_list = dict()
        self.transactions_for_detail = dict()
        self.terminal_authorizations = dict()
        self.cards = dict()

        JST = timezone(timedelta(hours=+9), 'JST')

        # 店舗情報
        shop_1 = mock.MagicMock(shop_number=1, shop_name='shop_1')
        shop_2 = mock.MagicMock(shop_number=2, shop_name='shop_2')

        # 企業情報
        company_1 = mock.MagicMock(company_number=1, company_name='company_1')
        company_2 = mock.MagicMock(company_number=2, company_name='company_2')

        # 端末情報
        terminal_1 = mock.MagicMock(terminal_no='1')
        terminal_2 = mock.MagicMock(terminal_no='2')

        campaign = mock.MagicMock(
            account_to_granted='99999999999', grant_amount=2000)

        card_in_transaction_1 = mock.MagicMock(
            card_config_name='card_config_name',
            card_no="9999999999990101",
            campaign=[campaign]
        )
        card_in_transaction_2 = mock.MagicMock(
            card_config_name='card_config_name',
            card_no='9999999999990102',
            campaign=[campaign]
        )
        card_in_transaction_3 = mock.MagicMock(
            card_config_name='card_config_name',
            card_no='9999999999990103',
            campaign=[campaign]
        )

        merge_source = mock.MagicMock(
            card_config_name='card_config_name',
            card_no='9999999999990102'
        )
        merge_target = mock.MagicMock(
            card_config_name='card_config_name',
            card_no='9999999999990101'
        )
        card_merge = mock.MagicMock(
            merge_source=merge_source,
            merge_target=merge_target)

        transaction_details_1 = mock.MagicMock(
            transaction_amount=100000, value_transaction_fluctuate_amount=2000,
            payable_bonus_fluctuate_amount=100,
            product_exchange_bonus_fluctuate_amount=3000)
        transaction_details_2 = mock.MagicMock(
            transaction_amount=200000, value_transaction_fluctuate_amount=3000,
            payable_bonus_fluctuate_amount=100,
            product_exchange_bonus_fluctuate_amount=4000)
        transaction_details_3 = mock.MagicMock(
            transaction_amount=200000, value_transaction_fluctuate_amount=3000,
            payable_bonus_fluctuate_amount=100,
            product_exchange_bonus_fluctuate_amount=4000)
        transaction_details_4 = mock.MagicMock(
            transaction_amount=300000, value_transaction_fluctuate_amount=4000,
            payable_bonus_fluctuate_amount=100,
            product_exchange_bonus_fluctuate_amount=5000)

        # フェーズ1ではMock内に必要な情報のすべてを持っている前提で設定する。
        # モデル定義後書き換える。
        transaction_1 = mock.MagicMock(
            magnetic_information='magnetic_information_1',
            card_merge=card_merge,
            card=[card_in_transaction_1, card_in_transaction_3],
            transaction_type=1,
            transaction_at=datetime(2021, 7, 4, 12, 30, tzinfo=JST),
            transaction_status=1, transaction_number=1,
            transaction=transaction_details_1,
            company=company_1,
            shop=shop_1,
            terminal=terminal_1)
        transaction_2 = mock.MagicMock(
            magnetic_information='magnetic_information_1',
            card_merge=card_merge,
            card=[card_in_transaction_1, card_in_transaction_2],
            transaction_type=1,
            transaction_at=datetime(2021, 7, 6, 12, 30, tzinfo=JST),
            transaction_status=1, transaction_number=2,
            transaction=transaction_details_2,
            company=company_2,
            shop=shop_2,
            terminal=terminal_1)
        transaction_3 = mock.MagicMock(
            magnetic_information='magnetic_information_1',
            card_merge=card_merge,
            card=[card_in_transaction_1, card_in_transaction_3],
            transaction_type=1,
            transaction_at=datetime(2021, 7, 4, 12, 30, tzinfo=JST),
            transaction_status=1, transaction_number=3,
            transaction=transaction_details_1,
            company=company_1,
            shop=shop_1,
            terminal=terminal_1)
        transaction_4 = mock.MagicMock(
            magnetic_information='magnetic_information_1',
            card_merge=card_merge,
            card=[card_in_transaction_1, card_in_transaction_2],
            transaction_type=2,
            transaction_at=datetime(2021, 7, 6, 12, 30, tzinfo=JST),
            transaction_status=1, transaction_number=4,
            transaction=transaction_details_2,
            company=company_2,
            shop=shop_2,
            terminal=terminal_1)
        transaction_5 = mock.MagicMock(
            magnetic_information='magnetic_information_1', card_merge=None,
            card=[card_in_transaction_2],
            transaction_type=1,
            transaction_at=datetime(2021, 7, 3, 12, 30, tzinfo=JST),
            transaction_status=1, transaction_number=5,
            transaction=transaction_details_3,
            company=company_1,
            shop=shop_1,
            terminal=terminal_1)
        transaction_6 = mock.MagicMock(
            magnetic_information='magnetic_information_1',
            card_merge=card_merge,
            card=[card_in_transaction_3],
            transaction_type=2,
            transaction_at=datetime(2021, 7, 3, 12, 30, tzinfo=JST),
            transaction_status=2, transaction_number=6,
            transaction=transaction_details_4,
            company=company_2,
            shop=shop_2,
            terminal=terminal_1)
        transaction_7 = mock.MagicMock(
            magnetic_information='magnetic_information_1',
            card_merge=card_merge,
            card=[card_in_transaction_3],
            transaction_type=2,
            transaction_at=datetime(2021, 7, 3, 12, 30, tzinfo=JST),
            transaction_status=2, transaction_number=7,
            transaction=transaction_details_4,
            company=company_2,
            shop=shop_2,
            terminal=terminal_2)

        # 取引履歴一覧取得のための取引履歴は端末番号ごとにリストに格納する。
        for transaction in [
            transaction_1, transaction_2, transaction_3,
            transaction_4, transaction_5, transaction_6,
            transaction_7
        ]:
            key = transaction.terminal.terminal_no
            if key not in self.transactions_for_list:
                self.transactions_for_list[key] = [transaction]
            else:
                self.transactions_for_list[key].append(transaction)

        # 取引履歴詳細取得のための取引履歴は取引番号をキーに辞書に格納する。
        for transaction_for_detail in [
            transaction_1, transaction_2, transaction_3,
            transaction_4, transaction_5, transaction_6,
            transaction_7
        ]:
            key = transaction_for_detail.transaction_number
            self.transactions_for_detail[key] = transaction_for_detail

        # 店舗端末認証情報
        terminal_authorization_1 = mock.MagicMock(
            terminal_no='1',
            access_token='header.payload.terminal_1',
            access_token_expires_at=to_utc_timestamp(
                datetime(2025, 7, 31, 12, 0, 0))
        )
        terminal_authorization_2 = mock.MagicMock(
            terminal_no='2',
            access_token='header.payload.terminal_2',
            access_token_expires_at=to_utc_timestamp(
                datetime(2021, 7, 1, 12, 0, 0))
        )
        for terminal_authorization in [
            terminal_authorization_1, terminal_authorization_2,
        ]:
            key = terminal_authorization.access_token
            self.terminal_authorizations[key] = terminal_authorization

        card_101 = mock.MagicMock(
            card_no='9999999999990101', card_pin='0101', state=1,
            payment=True, service_user_policy=True,
            provider_id='110000001', company_user_policy=True)
        card_102 = mock.MagicMock(
            card_no='9999999999990102', card_pin='0102', state=2,
            payment=True, service_user_policy=False,
            provider_id='110000001', company_user_policy=True)
        card_103 = mock.MagicMock(
            card_no='9999999999990103', card_pin='0103', state=1,
            payment=True, service_user_policy=True,
            provider_id='110000001', company_user_policy=True)

        for card in [card_101, card_102, card_103]:
            key = card.card_no
            self.cards[key] = card

    def get_card(self, card_number):
        '''カード情報を取得する.

            カード情報を取得する.

        Args:
            card_no (str型): カード番号.

        Returns:
            カード情報: 指定されたカード番号のモックオブジェクトがなければ、例外を発生させる.

        Raises:
            Exception: リクエストされたカード番号＆PINで一致するカードがない

        '''
        key = card_number
        try:
            card = self.cards[key]
        except KeyError:
            raise Exception('リクエストされたカード番号で一致するカードがない')
        return card

    def get_terminal_authorization(self, terminal_access_token):
        '''店舗端末認証情報を取得する.

            認証トークン及び端末番号に一致するカードを取得する

        Args:
            terminal_access_token (str型): 認証トークン
            terminal_no (str型): 端末番号

        Returns:
            店舗端末認証情報: 指定された認証トークンに一致するモックオブジェクトがなければ、例外を発生させる.

        Raises:
            Exception: リクエストされた認証トークンと端末番号で一致する店舗端末認証情報がない
            Exception: リクエストされた認証トークンで一致する店舗端末認証情報がない

        '''

        key = terminal_access_token
        try:
            terminal_authorization = self.terminal_authorizations[key]
        except KeyError:
            raise Exception('リクエストされた認証トークンで一致する店舗端末認証情報がない')
        return terminal_authorization

    def get_transaction_list(
        self, authorization_terminal_no, transaction_type, transaction_start, transaction_end, transaction_status,
        terminal_no, card_no, magnetic_information
    ):
        '''取引履歴一覧情報を取得する.
            取引履歴一覧情報を取得する.
        Args:
            authorization_terminal_no (str): 認証トークンから取得した端末番号
            transaction_type (int): リクエストから取得した取引種別
            transaction_start (DateTime): リクエストから取得した取引日時（From）
            transaction_end (DateTime): リクエストから取得した取引日時（To）
            transaction_status (int): リクエストから取得した取引ステータス
            terminal_no (str): リクエストから取得した端末番号
            card_no (str):  リクエストから取得したカード番号
            magnetic_information (str): リクエストから取得した磁気情報

        Returns:
            取引履歴一覧情報: 指定された検索条件、端末番号のオブジェクトがなければ、空のリストを返却する。
        '''

        # 端末番号での抽出
        transaction_list = self.transactions_for_list.get(authorization_terminal_no, [])
        response_transaction = []
        for transaction in transaction_list:
            # search_criteria内の各項目は、定義されていないこともある。
            # 各parameterの値がNoneの場合は、抽出に使用しない。
            # 取引種別での抽出
            if transaction_type and transaction.transaction_type != transaction_type:
                continue
            # 取引ステータスでの抽出
            if transaction_status and transaction.transaction_status != transaction_status:
                continue
            # 端末番号での抽出
            if terminal_no and transaction.terminal.terminal_no != terminal_no:
                continue
            # 磁気情報での抽出
            if magnetic_information and transaction.magnetic_information != magnetic_information:
                continue
            # カード番号での抽出
            if card_no:
                card_flag = False
                for card_data in transaction.card:
                    if card_data.card_no == card_no:
                        card_flag = True
                        break
                if not card_flag:
                    continue

            # 開始日時と終了日時からの抽出
            # どちらも設定されている。
            if transaction_start and transaction_end:
                if transaction_start <= transaction.transaction_at <= transaction_end:
                    response_transaction.append(transaction)
            # 開始日時のみ設定されている。
            elif transaction_start and not transaction_end:
                if transaction_start <= transaction.transaction_at:
                    response_transaction.append(transaction)
            # 終了日時のみ設定されている。
            elif not transaction_start and transaction_end:
                if transaction.transaction_at <= transaction_end:
                    response_transaction.append(transaction)
            # どちらも設定されていない。
            else:
                response_transaction.append(transaction)

        return response_transaction

    def get_transaction(self, transaction_number):
        '''取引履歴詳細情報を取得する.
            取引履歴詳細情報を取得する.
        Args:
            transaction_id (int型): 取引番号.
        Returns:
            取引履歴詳細情報: 指定されたカード番号、取引番号のモックオブジェクトがなければ、Noneを返却する.
        '''
        key = transaction_number
        try:
            transaction = self.transactions_for_detail[key]
        except KeyError:
            raise Exception('リクエストされた取引番号で一致する取引履歴がない')
        return transaction
