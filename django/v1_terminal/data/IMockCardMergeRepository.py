from v1_terminal.data.ICardMergeRepository import ICardMergeRepository

from v1_card.data.IAccessTokenRepository import IAccessTokenRepository
from v1_terminal.data.ITerminalAccessTokenRepository import \
    ITerminalAccessTokenRepository

from v1_terminal.buisiness_logic.DTO.card_merge_response \
    import CardMergeAmount, CardMergeBalanceSummary, CardMergeCard, CardMergeResponse

from unittest import mock

from utils.datetime_utility import get_datetime


class IMockCardMergeRepository(ICardMergeRepository):
    '''カード付替のモックを操作するクラス

        Attributes:
            card_access_token_repository (IMockAccessTokenRepository型)
            terminal_access_token_repository (IMockTerminalAccessTokenRepository型)
            transaction_history (dict型): 取引履歴を保持する.
            card_transaction_history (dict型): カード取引履歴を保持する.
            campaign_history (dict型): キャンペーン適用履歴を保持する.
    '''

    def __init__(self, card_access_token_repository: IAccessTokenRepository,
                 terminal_access_token_repository: ITerminalAccessTokenRepository):

        self.card_access_token_repository: \
            IAccessTokenRepository = card_access_token_repository
        self.terminal_access_token_repository: \
            ITerminalAccessTokenRepository = terminal_access_token_repository

        self.__prepare_card()
        self.__prepare_terminal()

        self.balance_summary: dict = dict()

    def __prepare_card(self):
        '''カード付替用のカード情報を用意する.

        Args:
            なし
        Returns:
            なし
        '''
        # カード設定
        card_config_01 = mock.MagicMock(
            id='card_config_01',
            config_name='card_config_01',
            value_balance_limit=50000,
            payable_bonus_balance_limit=50000,
            product_exchange_bonus_balance_limit=50000
        )
        card_config_02 = mock.MagicMock(
            id='card_config_02',
            config_name='card_config_02',
            value_balance_limit=25000,
            payable_bonus_balance_limit=25000,
            product_exchange_bonus_balance_limit=25000
        )
        card_config_03 = mock.MagicMock(
            id='card_config_03',
            config_name='card_config_03',
            value_balance_limit=25000,
            payable_bonus_balance_limit=5000,
            product_exchange_bonus_balance_limit=25000
        )

        # カード
        card_901 = mock.MagicMock(
            id='card_901_id',
            card_no='9999999999990901', card_pin='0901', state=1,
            card_config=card_config_01,
            payment=True,
            service_user_policy=True,
            company_user_policy=True,
            provider_id='01')

        card_902 = mock.MagicMock(
            id='card_902_id',
            card_no='9999999999990902', card_pin='0902', state=1,
            card_config=card_config_01,
            payment=True,
            service_user_policy=True,
            company_user_policy=True,
            provider_id='01')

        card_903 = mock.MagicMock(
            id='card_903_id',
            card_no='9999999999990903', card_pin='0903', state=1,
            card_config=card_config_02,
            payment=True,
            service_user_policy=True,
            company_user_policy=True,
            provider_id='01')

        card_904 = mock.MagicMock(
            id='card_904_id',
            card_no='9999999999990904', card_pin='0904', state=1,
            card_config=card_config_03,
            payment=True,
            service_user_policy=True,
            company_user_policy=True,
            provider_id='01')

        card_905 = mock.MagicMock(
            id='card_905_id',
            card_no='9999999999990905', card_pin='0905', state=1,
            card_config=card_config_03,
            payment=True,
            service_user_policy=True,
            company_user_policy=True,
            provider_id='01')

        card_906 = mock.MagicMock(
            id='card_906_id',
            card_no='9999999999990906', card_pin='0906', state=1,
            card_config=card_config_03,
            payment=True,
            service_user_policy=True,
            company_user_policy=True,
            provider_id='01')

        for card in [card_901, card_902, card_903, card_904, card_905, card_906]:
            key = card.card_no
            self.card_access_token_repository.cards[key] = card

        # 前払いバリュー 設定 ----------------------------------------------------

        # チャージバリュー設定 1
        charge_value_config_01 = mock.MagicMock(
            id='charge_value_conifg_01',
            value_type=0,
            start_available_date=get_datetime(2021, 4, 1, 12, 0, 0),
            end_available_date=get_datetime(2021, 9, 1, 12, 0, 0)
        )
        # チャージバリュー設定 2
        charge_value_config_02 = mock.MagicMock(
            id='charge_value_conifg_02',
            value_type=0,
            start_available_date=get_datetime(2021, 7, 1, 12, 0, 0),
            end_available_date=get_datetime(2021, 12, 1, 12, 0, 0)
        )

        # 強制付与バリュー設定 1
        grant_value_config_01 = mock.MagicMock(
            id='grant_value_config_01',
            value_type=1,
            start_available_date=get_datetime(2021, 4, 1, 12, 0, 0),
            end_available_date=get_datetime(2021, 9, 1, 12, 0, 0)
        )

        # ギフトバリュー設定 1
        gift_value_config_01 = mock.MagicMock(
            id='gift_value_config_01',
            value_type=2,
            start_available_date=get_datetime(2021, 6, 1, 12, 0, 0),
            end_available_date=get_datetime(2021, 11, 1, 12, 0, 0)
        )

        self.value_configs = [
            charge_value_config_01, charge_value_config_02,
            grant_value_config_01,
            gift_value_config_01]

        # 決済併用ボーナス 設定 ----------------------------------------------------

        # チャージボーナス設定 1
        charge_bonus_config_01 = mock.MagicMock(
            id='charge_bonus_config_01',
            bonus_type=0,
            start_available_date=get_datetime(2021, 4, 1, 12, 0, 0),
            end_available_date=get_datetime(2021, 9, 1, 12, 0, 0)
        )

        self.bonus_configs = [charge_bonus_config_01]

        # 残高情報 ------------------------------------------------------------------

        # チャージバリューの残高
        card_balance_0001 = mock.MagicMock(
            id='card_balance_0001',
            card_id=card_901.id,
            balance_type=0,
            balance=10000,
            value_config_id=charge_value_config_01.id,
            bonus_config_id=None
        )
        card_balance_0002 = mock.MagicMock(
            id='card_balance_0002',
            card_id=card_902.id,
            balance_type=0,
            balance=20000,
            value_config_id=charge_value_config_02.id,
            bonus_config_id=None
        )
        card_balance_0003 = mock.MagicMock(
            id='card_balance_0003',
            card_id=card_903.id,
            balance_type=0,
            balance=25000,
            value_config_id=charge_value_config_02.id,
            bonus_config_id=None
        )
        card_balance_0004 = mock.MagicMock(
            id='card_balance_0004',
            card_id=card_904.id,
            balance_type=0,
            balance=5000,
            value_config_id=charge_value_config_01.id,
            bonus_config_id=None
        )
        card_balance_0005 = mock.MagicMock(
            id='card_balance_0005',
            card_id=card_905.id,
            balance_type=0,
            balance=13000,
            value_config_id=charge_value_config_01.id,
            bonus_config_id=None
        )
        card_balance_0006 = mock.MagicMock(
            id='card_balance_0005',
            card_id=card_905.id,
            balance_type=0,
            balance=3000,
            value_config_id=charge_value_config_01.id,
            bonus_config_id=None
        )

        # 強制付与バリューの残高
        card_balance_0101 = mock.MagicMock(
            id='card_balance_0101',
            card_id=card_901.id,
            balance_type=0,
            balance=2000,
            value_config_id=grant_value_config_01.id,
            bonus_config_id=None
        )
        # ギフトバリューの残高
        card_balance_0201 = mock.MagicMock(
            id='card_balance_0201',
            card_id=card_901.id,
            balance_type=0,
            balance=5000,
            value_config_id=charge_value_config_02.id,
            bonus_config_id=None
        )

        # チャージボーナスの残高
        card_balance_1001 = mock.MagicMock(
            id='card_balance_1001',
            card_id=card_904.id,
            balance_type=1,
            balance=2000,
            value_config_id=None,
            bonus_config_id=charge_bonus_config_01.id
        )
        # チャージボーナスの残高
        card_balance_1002 = mock.MagicMock(
            id='card_balance_1002',
            card_id=card_905.id,
            balance_type=1,
            balance=2000,
            value_config_id=None,
            bonus_config_id=charge_bonus_config_01.id
        )
        # チャージボーナスの残高
        card_balance_1003 = mock.MagicMock(
            id='card_balance_1003',
            card_id=card_906.id,
            balance_type=1,
            balance=5000,
            value_config_id=None,
            bonus_config_id=charge_bonus_config_01.id
        )

        self.card_balances = [
            card_balance_0001, card_balance_0002, card_balance_0003, card_balance_0004, card_balance_0005,
            card_balance_0006,
            card_balance_0101,
            card_balance_0201,
            card_balance_1001, card_balance_1002, card_balance_1003
        ]

    def __prepare_terminal(self):
        '''取引用の店舗端末情報を用意する.

        Args:
            なし
        Returns:
            なし
        '''

        # 店舗端末を操作するユーザー
        user_01 = mock.MagicMock(
            mail_address='terminal.user.01@example.co.jp', password='terminal.user.01.password',
            authority_to_use_terminal=True
        )

        # 店舗端末を操作するユーザー
        user_99 = mock.MagicMock(
            mail_address='terminal.user.99@example.co.jp', password='terminal.user.99.password',
            authority_to_use_terminal=True
        )

        # 店舗端末
        terminal = mock.MagicMock(
            company_user_policy=True, state=1,
            users=[user_01],
            provider_id='01',
            company_id='01-01',
            shop_id='01-01-01',
            terminal_no='01-01-01-01',
            )
        key = terminal.terminal_no
        self.terminal_access_token_repository.terminals[key] = terminal

        # 取引取消を行う店舗端末
        terminal = mock.MagicMock(
            company_user_policy=True, state=1,
            users=[user_99],
            provider_id='01',
            company_id='01-01',
            shop_id='01-01-99',
            terminal_no='01-01-99-99'
            )

    def get_card_balances(self, card_id, balance_type):
        '''残高情報のリストを取得する.

        Args:
            card_id (str型): カードID
            balance_type (int型): 残高種別
        Returns:
            残高情報リスト (list型):
        '''
        balances = list()
        for card_balance in self.card_balances:
            if card_balance.card_id == card_id and \
               card_balance.balance_type == balance_type:
                balances.append(card_balance)
        return balances

    def get_value_config(self, value_config_id):
        '''バリュー設定を取得する.

        Args:
            value_config_id (str型): バリュー設定ID
        Returns:
            バリュー設定 (MagicMock型): 指定されたバリュー設定IDに一致するバリュー設定を取得する.
                                        一致するものがなければ、例外を発生する.
        Raises:
            Exception('リクエストされたバリュー設定IDに一致するバリュー設定情報がない')
        '''
        _value_config_id = value_config_id if value_config_id else ''
        if len(_value_config_id) == 0:
            raise Exception('リクエストされたバリュー設定IDに一致するバリュー設定情報がない')

        for value_config in self.value_configs:
            if value_config.id == _value_config_id:
                return value_config
        raise Exception('リクエストされたバリュー設定IDに一致するバリュー設定情報がない')

    def get_bonus_config(self, bonus_config_id):
        '''ボーナス設定を取得する.

        Args:
            bonus_config_id (str型): ボーナス設定ID
        Returns:
            ボーナス設定 (MagicMock型): 指定されたボーナス設定IDに一致するボーナス設定を取得する.
                                        一致するものがなければ、例外を発生する.
        Raises:
            Exception('リクエストされたボーナス設定IDに一致するボーナス設定情報がない')
        '''
        _bonus_config_id = bonus_config_id if bonus_config_id else ''
        if len(_bonus_config_id) == 0:
            raise Exception('リクエストされたボーナス設定IDに一致するバリュー設定情報がない')

        for bonus_config in self.bonus_configs:
            if bonus_config.id == _bonus_config_id:
                return bonus_config
        raise Exception('リクエストされたボーナス設定IDに一致するバリュー設定情報がない')

    def enumerate_balance_list(self, balance_list, balance_type, value_or_bonus_type):
        '''残高情報リストからバリュー設定またはボーナス設定を取得する.

        Args:
            balance_list (list型): 残高情報リスト
            balance_type (int型): 残高種別
            value_or_bonus_type (int型): バリュー種別またはボーナス種別
        Returns:
            バリュー設定またはボーナス設定 (MagicMock型):
                    残高情報リストから指定された残高種別をもつ残高情報を検索し、
                    バリュー種別に一致するボーナス設定、またはボーナス種別に一致するボーナス設定を返す.
                    一致するものがなければ、Noneを返す.
        '''
        for index, balance in enumerate(balance_list):
            try:
                if balance_type == 0:
                    value_config = self.get_value_config(balance.value_config_id)
                    if value_config.value_type == value_or_bonus_type:
                        return (index, value_config)
                else:
                    bonus_config = self.get_bonus_config(balance.bonus_config_id)
                    if bonus_config.bonus_type == value_or_bonus_type:
                        return (index, bonus_config)
            except Exception:
                continue
        return (-1, None)

    def merge_value(self, merge_from, merge_to):
        '''前払いバリューを付け替える.

        Args:
            merge_from (dict型): 付替元のカード番号、カードPIN番号を含む
            merge_to (dict型): 付替先のカード番号、カードPIN番号を含む
        Returns:
        '''

        # カード情報を取得する
        card_from = self.card_access_token_repository.get_card(
            merge_from['card_no']
        )
        card_to = self.card_access_token_repository.get_card(
            merge_to['card_no']
        )

        # 残高種別 前払いバリュー(0)
        # 前払いバリュー [チャージバリュー(0), 強制付与バリュー(1), ギフトバリュー(2),
        #                   資金移動バリュー(10), 特別指定バリュー(20)]

        # 前払いバリュー: 最大5個の残高情報がある

        balance_type = 0

        # 付替元カード残高情報を取得する（リスト）
        card_balances_from = self.get_card_balances(card_from.id, balance_type)

        # 付替元に残高情報がない
        if card_balances_from.count == 0:
            return

        # 付替先カード残高情報を取得する（リスト）
        card_balances_to = self.get_card_balances(card_to.id, balance_type)

        if card_balances_to.count == 0:
            # 付替元の残高情報を付替先に書き換える
            for card in card_balances_from:
                card.card_id = card_to.id
        else:
            for card_balance_from in card_balances_from:
                # 付替元のバリュー設定情報情報を取得する
                value_config_from = self.get_value_config(card_balance_from.value_config_id)
                # 付替先の残高情報リストから、付替元と同種のバリュー設定を取得する
                index, value_config_to = \
                    self.enumerate_balance_list(
                        card_balances_to, balance_type, value_config_from.value_type)
                if index == -1:
                    # 付替元と同種の残高情報が付替先にない
                    # 付替元の残高情報を付替先に書き換える
                    card_balance_from.card_id = card_to.id
                else:
                    # 付替元と同種の残高情報を付替先が持つ
                    card_balance_to = card_balances_to[index]

                    # 残高を加算する
                    card_balance_to.balance += card_balance_from.balance
                    # 付替元の残高を0にする
                    card_balance_from.balance = 0

                    # 有効期限
                    # 付替元、付替先でカード設定が同一
                    if card_from.card_config.id == card_to.card_config.id:
                        # 付替元の有効期限をそのまま付替先の有効期限とする
                        card_balance_to.end_available_date = card_balance_from.end_available_date
                    else:
                        card_config_from = self.get_value_config(card_balance_from.value_config_id)
                        card_config_to = self.get_value_config(card_balance_to.value_config_id)

                        # 有効期限の短い方を付替先の有効期限とする
                        new_end_available_date = min(expire_at for expire_at in [
                            card_config_from.end_available_date,
                            card_config_to.end_available_date
                            ])
                        card_balance_to.end_avaliable_date = new_end_available_date

        # 付替元、付替先でカード設定が同一
        if card_from.card_config.id == card_to.card_config.id:
            # 付替元を付替済み(8)に変更する
            card_from.state = 8

    def merge_bonus(self, merge_from, merge_to):
        '''ボーナスを付け替える.

        Args:
            merge_from (dict型): 付替元のカード番号、カードPIN番号を含む
            merge_to (dict型): 付替先のカード番号、カードPIN番号を含む
        Returns:
        '''

        # カード情報を取得する
        card_from = self.card_access_token_repository.get_card(
            merge_from['card_no']
        )
        card_to = self.card_access_token_repository.get_card(
            merge_to['card_no']
        )
        # 付替元、付替先でカード設定が異なる
        # 決済併用ボーナス、商品交換ボーナスを統合しない
        if card_from.card_config.id != card_to.card_config.id:
            return

        # 残高種別 決済併用ボーナス(1), 商品交換ボーナス(2)
        # 決済併用ボーナス [チャージボーナス(0), 決済ボーナス(1), 強制付与ボーナス(2), ギフトボーナス(3)]

        # 決済併用ボーナス: 最大4個の残高情報がある
        # 商品交換ボーナス: 最大1個の残高情報がある
        for balance_type in [1, 2]:
            # 付替元カード残高情報を取得する（リスト）
            card_balances_from = self.get_card_balances(card_from.id, balance_type)

            # 付替元に残高情報がない
            if card_balances_from.count == 0:
                continue

            # 付替先カード残高情報を取得する（リスト）
            card_balances_to = self.get_card_balances(card_to.id, balance_type)

            if card_balances_to.count == 0:
                # 付替元の残高情報を付替先に書き換える
                for card in card_balances_from:
                    card.card_id = card_to.id
            else:
                for card_balance_from in card_balances_from:

                    # 付替元のボーナス設定情報を取得する
                    bonus_config_from = self.get_bonus_config(card_balance_from.bonus_config_id)
                    # 付替先の残高情報リストから、付替元と同種のボーナス設定を取得する
                    index, bonus_config_to = \
                        self.enumerate_balance_list(
                            card_balances_to, balance_type, bonus_config_from.bonus_type)

                    if index == -1:
                        # 付替元と同種の残高情報が付替先にない
                        # 付替元の残高情報を付替先に書き換える
                        card_balance_from.card_id = card_to.id
                    else:
                        # 付替元と同種の残高情報を付替先が持つ
                        card_balance_to = card_balances_to[index]

                        # 残高を加算する
                        card_balance_to.balance += card_balance_from.balance
                        # 付替元の残高を0にする
                        card_balance_from.balance = 0

                        # 付替元の有効期限をそのまま付替先の有効期限とする
                        card_balance_to.end_avaliable_date = card_balance_from.end_available_date
        # 付替元、付替先でカード設定が同一
        if card_from.card_config.id == card_to.card_config.id:
            # 付替元を付替済み(8)に変更する
            card_from.state = 8

    def verify_over_limit(self, merge_from, merge_to):
        '''付替可能かを検証する.

        Args:
            merge_from (dict型): 付替元のカード番号、カードPIN番号を含む
            merge_to (dict型): 付替先のカード番号、カードPIN番号を含む
        Returns:
            True: カードは付替可能である
            False: カードは付替可能ではない
        '''
        # カード情報を取得する
        card_from = self.card_access_token_repository.get_card(
            merge_from['card_no']
        )
        card_to = self.card_access_token_repository.get_card(
            merge_to['card_no']
        )
        for balance_type in [0, 1, 2]:
            if balance_type == 0:
                limit_balance = card_to.card_config.value_balance_limit
            elif balance_type == 1:
                limit_balance = card_to.card_config.payable_bonus_balance_limit
            elif balance_type == 2:
                limit_balance = card_to.card_config.product_exchange_bonus_balance_limit

            # 付替元カード残高情報を取得する（リスト）
            card_balances_from = self.get_card_balances(card_from.id, balance_type)

            # 付替先カード残高情報を取得する（リスト）
            card_balances_to = self.get_card_balances(card_to.id, balance_type)

            sum_balance = sum([balance.balance for balance in card_balances_from]) + \
                sum([balance.balance for balance in card_balances_to])

            if sum_balance > limit_balance:
                # 付替先の残高上限値を超えている
                return False
        return True

    def get_summary(self, key_name, merge_from, merge_to):
        '''残高に関するサマリーを取得する.　レスポンス用

        Args:
            key_name (str型): self.balance_summaryのキー名
            merge_from (dict型): 付替元のカード番号、カードPIN番号を含む
            merge_to (dict型): 付替先のカード番号、カードPIN番号を含む
        Returns:
            なし
        '''
        # カード情報を取得する
        card_from = self.card_access_token_repository.get_card(
            merge_from['card_no']
        )
        card_to = self.card_access_token_repository.get_card(
            merge_to['card_no']
        )

        self.balance_summary['source_card'] = dict()
        self.balance_summary['source_card']['config_name'] = card_from.card_config.config_name
        self.balance_summary['source_card']['card_no'] = card_from.card_no
        self.balance_summary['destination_card'] = dict()
        self.balance_summary['destination_card']['config_name'] = card_to.card_config.config_name
        self.balance_summary['destination_card']['card_no'] = card_to.card_no

        sum_balance_dict = dict()
        sum_balance_dict['from'] = dict()
        sum_balance_dict['to'] = dict()

        for balance_type in [0, 1, 2]:

            # 付替元カード残高情報を取得する（リスト）
            card_balances_from = self.get_card_balances(card_from.id, balance_type)
            # 付替先カード残高情報を取得する（リスト）
            card_balances_to = self.get_card_balances(card_to.id, balance_type)

            sum_balance_from = sum(balance.balance for balance in card_balances_from)
            sum_balance_to = sum(balance.balance for balance in card_balances_to)

            sum_balance_dict['from'][balance_type] = sum_balance_from
            sum_balance_dict['to'][balance_type] = sum_balance_to

        sum_balance_dict['from']['card_state'] = card_from.state
        sum_balance_dict['to']['card_state'] = card_to.state

        self.balance_summary[key_name] = sum_balance_dict

    def merge(self, merge_from, merge_to):
        '''前払いバリュー、ボーナスを付け替える.

        Args:
            merge_from (dict型): 付替元のカード番号、カードPIN番号を含む
            merge_to (dict型): 付替先のカード番号、カードPIN番号を含む
        Returns:
        '''
        # 付け替え可能か検証する
        if self.verify_over_limit(merge_from, merge_to):

            # 付け替え前の残高情報からレスポンス用データを作成する
            self.get_summary('before', merge_from, merge_to)
            # 前払いバリューを付け替える
            self.merge_value(merge_from, merge_to)
            # ボーナスを付け替える
            self.merge_bonus(merge_from, merge_to)

            # 付け替え後の残高情報からレスポンス用データを作成する
            self.get_summary('after', merge_from, merge_to)

            return self.make_response()
        else:
            return None

    def make_response(self):
        '''レスポンス用CardMergeResponseオブジェクトを返す

        Args:
            なし
        Returns:
            CardMergeResponseオブジェクト
        '''
        before = self.balance_summary['before']
        after = self.balance_summary['after']

        value_before_merge = before['from'][0]
        value_after_merge = after['from'][0]
        payable_bonus_before_merge = before['from'][1]
        payable_bonus_after_merge = after['from'][1]
        product_exchange_bonus_before_merge = before['from'][2]
        product_exchange_bonus_after_merge = after['from'][2]

        merged_amount = list()
        merged_amount.append(abs(value_before_merge - value_after_merge))
        merged_amount.append(abs(payable_bonus_before_merge - payable_bonus_after_merge))
        merged_amount.append(abs(product_exchange_bonus_before_merge - product_exchange_bonus_after_merge))

        # 有効期限(CardMergeBalanceSummary)に関しては、モデル定義後とする
        # バリュー種別ごと、ボーナス種別ごとに有効期限があるはず。
        # 前払いバリュー、決済併用ボーナス単位に有効期限を持っていないはずなので保留
        return CardMergeResponse(
            source_card=CardMergeCard(
                card_config_name=self.balance_summary['source_card']['config_name'],
                card_no=self.balance_summary['source_card']['card_no']
            ),
            destination_card=CardMergeCard(
                card_config_name=self.balance_summary['destination_card']['config_name'],
                card_no=self.balance_summary['destination_card']['card_no']
            ),
            merged_amount=CardMergeAmount(
                value_merged_amount=merged_amount[0],
                payable_bonus_merged_amount=merged_amount[1],
                product_exchage_bonus_merged_amount=merged_amount[2]
            ),
            source_before_merge=CardMergeBalanceSummary(
                card_state=before['from']['card_state'],
                value_amount=before['from'][0],
                payable_bonus_amount=before['from'][1],
                product_exchage_bonus_amount=before['from'][2]
            ),
            source_after_merge=CardMergeBalanceSummary(
                card_state=after['to']['card_state'],
                value_amount=before['to'][0],
                payable_bonus_amount=before['to'][1],
                product_exchage_bonus_amount=before['to'][2]
            ),
            destination_before_merge=CardMergeBalanceSummary(
                card_state=before['from']['card_state'],
                value_amount=before['from'][0],
                payable_bonus_amount=before['from'][1],
                product_exchage_bonus_amount=before['from'][2]
            ),
            destination_after_merge=CardMergeBalanceSummary(
                card_state=after['to']['card_state'],
                value_amount=after['to'][0],
                payable_bonus_amount=after['to'][1],
                product_exchage_bonus_amount=after['to'][2]
            )
        )
