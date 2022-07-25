import uuid
from unittest import mock

from utils.datetime_utility import get_datetime

from v1_card.data.IMockAccessTokenRepository import IMockAccessTokenRepository

from v1_terminal.data.IMockTerminalAccessTokenRepository import \
    IMockTerminalAccessTokenRepository

from v1_terminal.data.ITransactionCancelRepository import \
    ITransactionCancelRepository

from v1_terminal.buisiness_logic.DTO.transaction_cancel_response \
    import (
        TransactionCancelResponse,
        TransactionCancelCompany,
        TransactionCancelShop,
        TransactionCancelTransaction,
        TransactionCancelBalance,
        TransactionCancelCampaign,
        TransactionCancelCard,
    )
from utils.datetime_utility import now

import operator


class IMockTransactionCancelRepository(
    ITransactionCancelRepository
):
    '''取引取消のモックを操作するクラス

        Attributes:
            card_access_token_repository (IMockAccessTokenRepository型)
            terminal_access_token_repository (IMockTerminalAccessTokenRepository型)
            transaction_history (dict型): 取引履歴を保持する.
            card_transaction_history (dict型): カード取引履歴を保持する.
            campaign_history (dict型): キャンペーン適用履歴を保持する.
    '''

    def __init__(self, card_access_token_repository: IMockAccessTokenRepository,
                 terminal_access_token_repository: IMockTerminalAccessTokenRepository):

        self.card_access_token_repository: \
            IMockAccessTokenRepository = card_access_token_repository
        self.terminal_access_token_repository: \
            IMockTerminalAccessTokenRepository = terminal_access_token_repository

        self.__prepare_card()
        self.__prepare_transaction()
        self.__prepare_terminal()

        # # ボーナス
        # bonus_id = str(uuid.uuid4())

        # # キャンペーン適用履歴

        # campaign_history_id_01 = str(uuid.uuid4())

        # campaign_id_01 = str(uuid.uuid4())

        # # 決済併用ボーナス
        # campaign_01 = mock.MagicMock(
        #     id=campaign_history_id_01,
        #     campain_id=campaign_id_01,
        #     campain_name='test_campaign_000001',
        #     card_transaction_id=card_transaction_id_05,
        #     bonus_id=bonus_id,
        #     bonus_type=1,
        #     bonus_grant=500,
        #     expire_at=get_datetime(2021, 12, 31, 23, 59, 59)
        # )

        # # キャンペーン適用履歴
        # self.campaign_history = dict()
        # for campaign in [campaign_01]:
        #     key = campaign.card_transaction_id
        #     self.campaign_history[key] = campaign

    def __prepare_card(self):
        '''取引用のカード情報を用意する.

        Args:
            なし
        Returns:
            なし
        '''

        card_901 = mock.MagicMock(
            card_no='9999999999990901', card_pin='0901', state=1,
            config_name='card_config_name_9999999999990901',
            payment=True,
            service_user_policy=True,
            company_user_policy=True,
            provider_id='01')

        card_902 = mock.MagicMock(
            card_no='9999999999990902', card_pin='0902', state=1,
            config_name='card_config_name_9999999999990902',
            payment=True,
            service_user_policy=True,
            company_user_policy=True,
            provider_id='01')

        card_903 = mock.MagicMock(
            card_no='9999999999990903', card_pin='0903', state=1,
            config_name='card_config_name_9999999999990903',
            payment=True,
            service_user_policy=True,
            company_user_policy=True,
            provider_id='01')

        for card in [card_901, card_902, card_903]:
            key = card.card_no
            self.card_access_token_repository.cards[key] = card

    def __prepare_transaction(self):
        '''取引履歴を用意する.

        Args:
            なし
        Returns:
            なし
        '''

        # カード　9999999999990901　に対する取引 -----------------------------------------

        # チャージ　取引履歴
        transaction_history_id_0901_01 = '33d4b641-bf5b-415a-bc36-9f4cfdb07022'
        transaction_id_0901_01 = '9d2af7aa-cbc1-42f7-88c6-e71f3e08ee72'
        transaction_0901_01 = mock.MagicMock(
            id=transaction_history_id_0901_01,
            transaction_id=transaction_id_0901_01,
            user_id='901',
            transaction_at=get_datetime(2021, 7, 1, 12, 00, 00),
            transaction_type=0,
            provider_id='01',
            company_id='01-01',
            shop_id='01-01-01',
            terminal_no='01-01-01-01',
            value_transaction_amount=10000,
            payable_bonus_transaction_amount=0,
            product_exchange_bonus_amount=0
        )
        # チャージ　カード取引履歴
        card_transaction_id_0901_01 = 'fb6ad167-c593-4fae-82b8-a8d442995c55'
        card_transaction_0901_01 = mock.MagicMock(
            id=card_transaction_id_0901_01,
            transaction_id=transaction_id_0901_01,
            transaction_at=get_datetime(2021, 7, 1, 12, 00, 00),
            transaction_type=0,
            card_no='9999999999990901',
            card_config_id='9999999999990901-01',
            provider_id='01',
            company_id='01-01',
            shop_id='01-01-01',
            terminal_no='01-01-01-01',
            value_transaction_amount=10000,
            payable_bonus_transaction_amount=0,
            product_exchange_bonus_amount=0
        )

        # カード　9999999999990902　に対する取引 -----------------------------------------

        # チャージ　取引履歴
        transaction_history_id_0902_01 = '072b1834-7835-4747-b6f5-d5df11438d72'
        transaction_id_0902_01 = '9dca6863-8c9a-413d-8e98-85f688c57353'
        transaction_0902_01 = mock.MagicMock(
            id=transaction_history_id_0902_01,
            transaction_id=transaction_id_0902_01,
            user_id='902',
            transaction_at=get_datetime(2021, 7, 1, 12, 00, 00),
            transaction_type=0,
            provider_id='01',
            company_id='01-01',
            shop_id='01-01-01',
            terminal_no='01-01-01-01',
            value_transaction_amount=10000,
            payable_bonus_transaction_amount=0,
            product_exchange_bonus_amount=0
        )
        # チャージ　カード取引履歴
        card_transaction_id_0902_01 = 'c03c0764-f6a5-4ef4-b41b-9c519b7232a6'
        card_transaction_0902_01 = mock.MagicMock(
            id=card_transaction_id_0902_01,
            transaction_id=transaction_id_0902_01,
            transaction_at=get_datetime(2021, 7, 1, 12, 00, 00),
            transaction_type=0,
            card_no='9999999999990902',
            card_config_id='9999999999990902-01',
            provider_id='01',
            company_id='01-01',
            shop_id='01-01-01',
            terminal_no='01-01-01-01',
            value_transaction_amount=10000,
            payable_bonus_transaction_amount=0,
            product_exchange_bonus_amount=0
        )

        # 決済　取引履歴
        transaction_history_id_0902_02 = '3204f9a1-38ff-477a-a564-9134a5112b5c'
        transaction_id_0902_02 = '2e1d2a90-e2f7-416c-a7c0-5911d43aa6b7'
        transaction_0902_02 = mock.MagicMock(
            id=transaction_history_id_0902_02,
            transaction_id=transaction_id_0902_02,
            user_id='902',
            transaction_at=get_datetime(2021, 7, 1, 12, 30, 00),
            transaction_type=1,
            provider_id='01',
            company_id='01-01',
            shop_id='01-01-01',
            terminal_no='01-01-01-01',
            value_transaction_amount=5000,
            payable_bonus_transaction_amount=0,
            product_exchange_bonus_amount=0
        )
        # 決済　カード取引履歴
        card_transaction_id_0902_02 = 'bd5fe088-0350-4dee-b843-1b0c19f98b7f'
        card_transaction_0902_02 = mock.MagicMock(
            id=card_transaction_id_0902_02,
            transaction_id=transaction_id_0902_02,
            transaction_at=get_datetime(2021, 7, 1, 12, 30, 00),
            transaction_type=1,
            card_no='9999999999990902',
            card_config_id='9999999999990902-01',
            provider_id='01',
            company_id='01-01',
            shop_id='01-01-01',
            terminal_no='01-01-01-01',
            value_transaction_amount=-5000,
            payable_bonus_transaction_amount=0,
            product_exchange_bonus_amount=0
        )
        # ボーナス付与　取引履歴
        transaction_history_id_0902_03 = '879c89fd-adf6-4694-acd2-bef38f8ecb62'
        transaction_id_0902_03 = '052a3dc8-04e6-4584-ba07-af792fd44fc1'
        transaction_0902_03 = mock.MagicMock(
            id=transaction_history_id_0902_03,
            transaction_id=transaction_id_0902_03,
            user_id='902',
            transaction_at=get_datetime(2021, 7, 2, 12, 13, 00),
            transaction_type=2,
            card_no='9999999999990902',
            card_config_id='9999999999990902-01',
            provider_id='01',
            company_id='01-01',
            shop_id='01-01-01',
            terminal_no='01-01-01-01',
            value_transaction_amount=5000,
            payable_bonus_transaction_amount=1000,
            product_exchange_bonus_amount=0
        )
        # ボーナス付与　カード取引履歴
        card_transaction_id_0902_03 = 'aa9e5592-c4d3-472d-8484-55ee5b9ede80'
        card_transaction_0902_03 = mock.MagicMock(
            id=card_transaction_id_0902_03,
            transaction_id=transaction_id_0902_03,
            user_id='902',
            transaction_at=get_datetime(2021, 7, 2, 12, 13, 00),
            transaction_type=2,
            card_no='9999999999990902',
            card_config_id='9999999999990902-01',
            provider_id='01',
            company_id='01-01',
            shop_id='01-01-01',
            terminal_no='01-01-01-01',
            value_transaction_amount=0,
            payable_bonus_transaction_amount=1000,
            product_exchange_bonus_amount=0
        )

        # カード　9999999999990903　に対する取引 -----------------------------------------

        # チャージ　取引履歴
        transaction_history_id_0903_01 = 'f59aea9a-2f95-4f82-8396-288e6ceccc7f'
        transaction_id_0903_01 = '20d85ea3-5a1c-4113-a0df-ea6e93e03eb1'
        transaction_0903_01 = mock.MagicMock(
            id=transaction_history_id_0903_01,
            transaction_id=transaction_id_0903_01,
            user_id='903',
            transaction_at=get_datetime(2021, 7, 1, 12, 00, 00),
            transaction_type=0,
            provider_id='01',
            company_id='01-01',
            shop_id='01-01-01',
            terminal_no='01-01-01-01',
            value_transaction_amount=10000,
            payable_bonus_transaction_amount=0,
            product_exchange_bonus_amount=0
        )
        # チャージ　カード取引履歴
        card_transaction_id_0903_01 = 'a4e785db-ccba-4055-9131-4f16b0bf4ca6'
        card_transaction_0903_01 = mock.MagicMock(
            id=card_transaction_id_0903_01,
            transaction_id=transaction_id_0903_01,
            transaction_at=get_datetime(2021, 7, 1, 12, 00, 00),
            transaction_type=0,
            card_no='9999999999990903',
            card_config_id='9999999999990903-01',
            provider_id='01',
            company_id='01-01',
            shop_id='01-01-01',
            terminal_no='01-01-01-01',
            value_transaction_amount=10000,
            payable_bonus_transaction_amount=0,
            product_exchange_bonus_amount=0
        )
        # ボーナス付与　取引履歴
        transaction_history_id_0903_02 = 'ee615904-a49d-4ced-a06e-d35d991dcbc5'
        transaction_id_0903_02 = 'cb1fb51a-f495-4a14-8c09-43b12a84109f'
        transaction_0903_02 = mock.MagicMock(
            id=transaction_history_id_0903_02,
            transaction_id=transaction_id_0903_02,
            user_id='903',
            transaction_at=get_datetime(2021, 7, 2, 12, 13, 00),
            transaction_type=2,
            card_no='9999999999990903',
            card_config_id='9999999999990903-01',
            provider_id='01',
            company_id='01-01',
            shop_id='01-01-01',
            terminal_no='01-01-01-01',
            value_transaction_amount=10000,
            payable_bonus_transaction_amount=1000,
            product_exchange_bonus_amount=0
        )
        # ボーナス付与　カード取引履歴
        card_transaction_id_0903_02 = '582ca789-4114-47df-aecb-8ff15ba8b2b4'
        card_transaction_0903_02 = mock.MagicMock(
            id=card_transaction_id_0903_02,
            transaction_id=transaction_id_0903_02,
            user_id='903',
            transaction_at=get_datetime(2021, 7, 2, 12, 13, 00),
            transaction_type=2,
            card_no='9999999999990903',
            card_config_id='9999999999990903-01',
            provider_id='01',
            company_id='01-01',
            shop_id='01-01-01',
            terminal_no='01-01-01-01',
            value_transaction_amount=0,
            payable_bonus_transaction_amount=1000,
            product_exchange_bonus_amount=0
        )
        # ボーナス利用　取引履歴
        transaction_history_id_0903_03 = '3e55a4d6-3572-4553-a94d-05aba225f7a7'
        transaction_id_0903_03 = 'c39311f6-a762-4220-a31c-526deacdf48f'
        transaction_0903_03 = mock.MagicMock(
            id=transaction_history_id_0903_03,
            transaction_id=transaction_id_0903_03,
            user_id='903',
            transaction_at=get_datetime(2021, 7, 2, 12, 14, 00),
            transaction_type=2,
            card_no='9999999999990903',
            card_config_id='9999999999990903-01',
            provider_id='01',
            company_id='01-01',
            shop_id='01-01-01',
            terminal_no='01-01-01-01',
            value_transaction_amount=10000,
            payable_bonus_transaction_amount=200,
            product_exchange_bonus_amount=0
        )
        # ボーナス利用　カード取引履歴
        card_transaction_id_0903_03 = 'b7cd8046-fb70-46f1-91cb-3f7e00d9d519'
        card_transaction_0903_03 = mock.MagicMock(
            id=card_transaction_id_0903_03,
            transaction_id=transaction_id_0903_03,
            user_id='903',
            transaction_at=get_datetime(2021, 7, 2, 12, 14, 00),
            transaction_type=2,
            card_no='9999999999990903',
            card_config_id='9999999999990903-01',
            provider_id='01',
            company_id='01-01',
            shop_id='01-01-01',
            terminal_no='01-01-01-01',
            value_transaction_amount=0,
            payable_bonus_transaction_amount=-800,
            product_exchange_bonus_amount=0
        )

        self.transaction_history = [
            transaction_0901_01,
            transaction_0902_01, transaction_0902_02, transaction_0902_03,
            transaction_0903_01, transaction_0903_02, transaction_0903_03,
            ]

        self.card_transaction_history = [
            card_transaction_0901_01,
            card_transaction_0902_01, card_transaction_0902_02, card_transaction_0902_03,
            card_transaction_0903_01, card_transaction_0903_02, card_transaction_0903_03]

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
        for card_transaction in self.card_transaction_history:
            terminal = mock.MagicMock(
                terminal_no=card_transaction.terminal_no,
                company_user_policy=True, state=1,
                users=[user_01],
                provider_id=card_transaction.provider_id,
                company_id=card_transaction.campany_id,
                shop_id=card_transaction.shop_id
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

    def get_transaction(self, transaction_id):
        '''取引履歴から取引を取得する.

        Args:
            transaction_id (str型): 取引番号.

        Returns:
            取引履歴 (MagicMock型):
                リクエストされた取引番号で一致する取引履歴がない場合、例外を発生する.

        Raises:
            Exception: リクエストされた取引番号で一致する取引履歴がない

        '''
        for transaction in self.transaction_history:
            if transaction.transaction_id == transaction_id:
                return transaction

        raise Exception('リクエストされた取引番号で一致する取引がない')

    def get_or_create_transaction(self, transaction_id):
        '''指定の取引番号に紐づく取引履歴を取得する.または新しい取引を生成する.

        Args:
            transaction_id (str型): 取引番号.

        Returns:
            取引情報 (MagicMock型):
                リクエストされた取引番号で一致する取引がない場合、新しい取引履歴オブジェクトを返す.

        Raises:
            Exception: リクエストされた取引番号で一致する取引がない

        '''
        for transaction in self.transaction_history:
            if transaction.transaction_id == transaction_id:
                return transaction
        return mock.MagicMock()

    def get_card_transactions_by_transaction_id(self, transaction_id):
        '''指定の取引番号に紐づくカード取引履歴を取得する.

        Args:
            取引番号 (str型): 取引番号.

        Returns:
            カード取引履歴のリスト (MagicMock型のリスト):
                リクエストされた取引番号で一致するカード取引履歴がない場合
                空のリストを返す.
        '''
        card_transactions = list()
        for card_transaction in self.card_transaction_history:
            if card_transaction.transaction_id == transaction_id:
                card_transactions.append(card_transaction)
        return card_transactions

    def get_balances_from_card_transaction_list(self, card_transaction_list):
        '''指定のカード取引履歴リストの残高を取得する.

        Args:
            card_transaction_list (list型): カード取引履歴のリスト.

        Returns:
            残高 (tuple型):
                前払いバリュー残高
                決済併用ボーナス残高
                商品交換ボーナス残高
        '''
        value_transaction_amount = 0
        payable_bonus_transaction_amount = 0
        product_exchange_bonus_amount = 0

        return_none = True
        for card_transaction in card_transaction_list:
            value_transaction_amount += card_transaction.value_transaction_amount
            payable_bonus_transaction_amount += card_transaction.payable_bonus_transaction_amount
            product_exchange_bonus_amount += card_transaction.product_exchange_bonus_amount
            return_none = False

        if return_none:
            return None
        else:
            return (
                value_transaction_amount,
                payable_bonus_transaction_amount,
                product_exchange_bonus_amount
            )

    def get_balances_by_card_no(self, card_no):
        '''指定のカード番号に紐づくカード取引履歴の残高を取得する.

        Args:
            card_no (str型): カード番号.

        Returns:
            残高 (tuple型):
                前払いバリュー残高
                決済併用ボーナス残高
                商品交換ボーナス残高
        '''
        return_none = True
        card_transaction_list = list()
        for card_transaction in self.card_transaction_history:
            if card_transaction.card_no == card_no:
                card_transaction_list.append(card_transaction)
                return_none = False
        if return_none:
            return None
        else:
            return self.get_balances_from_card_transaction_list(card_transaction_list)

    def create_cancel_card_transaction(
                                    self,
                                    terminal,
                                    cancel_transaction,
                                    new_transaction_id,
                                    new_transaction_type,
                                    new_transaction_at):
        '''取消のカード取引を作成する.

        Args:
            terminal (MagicMock型): 店舗端末.
            cancel_transaction (MagicMock型): 取り消される側の取引
            new_transaction_id (str型): 取消のために発行された新しい取引番号
            new_transaction_type (int型): 取消後の取引種別
            new_transaction_at (datetime型): 取消の取引日時
        Returns:
            取消のカード取引リスト (list型):
        '''

        # 取引番号からカード取引履歴のリストを取得する。取り消される側
        card_transactions = \
            self.get_card_transactions_by_transaction_id(cancel_transaction.transaction_id)

        new_card_transactions = list()

        for card_transaction in card_transactions:
            # 取り消される側のカード取引から新しいカード取引を作成する
            new_card_transaction = mock.MagicMock(
                # 新規のID
                id=str(uuid.uuid4()),
                # 新しく採番された取引番号
                transaction_id=new_transaction_id,
                # 現日時
                transaction_at=new_transaction_at,
                # 取消の取引種別
                transaction_type=new_transaction_type,
                # 取り消される側から引き継ぐ情報
                card_no=card_transaction.card_no,
                card_config_id=card_transaction.card_config_id,
                # 取消を実行している店舗端末
                provider_id=terminal.provider_id,
                company_id=terminal.company_id,
                shop_id=terminal.shop_id,
                terminal_no=terminal.terminal_no,
                # 逆の増減
                value_transaction_amount=card_transaction.value_transaction_amount * (-1),
                payable_bonus_transaction_amount=card_transaction.payable_bonus_transaction_amount * (-1),
                product_exchange_bonus_amount=card_transaction.product_exchange_bonus_amount * (-1)
            )
            new_card_transactions.append(new_card_transaction)

        return new_card_transactions

    def create_cancel_transaction(self, terminal, new_transaction_id, cancel_target_transaction_id):
        '''取消の取引を作成する.

        Args:
            terminal (MagicMock型): 店舗端末.
            new_transaction_id (str型): 取消のために発行された新しい取引番号
            new_transaction_at (datetime型): 取消の取引日時
        Returns:
            取消処理の結果 (dict型):
        '''
        # 取引番号に紐づく取引履歴を取得する。取り消される側
        cancel_target_transaction = self.get_transaction(cancel_target_transaction_id)

        # 取引履歴の取引種別
        # チャージ(0)、決済(1)、ボーナス付与(2)、ボーナス利用(3)
        transaction_type = cancel_target_transaction.transaction_type
        if transaction_type == 0:
            # チャージ(0) → チャージ取消(4)
            new_transaction_type = 4
        elif transaction_type == 1:
            # 決済(1) → 決済取消(5)
            new_transaction_type = 5
        elif transaction_type == 2:
            # ボーナス付与(2) → ボーナス付与取消(6)
            new_transaction_type = 6
        elif transaction_type == 3:
            # ボーナス利用(3) → ボーナス利用取消(7)
            new_transaction_type = 7
        else:
            pass

        new_transaction_at = now()

        # 取消のカード取引を取得
        new_card_transaction_list = \
            self.create_cancel_card_transaction(
                terminal, cancel_target_transaction,
                new_transaction_id, new_transaction_type, new_transaction_at)

        # 取消のカード取引残高を取得
        balance = self.get_balances_from_card_transaction_list(new_card_transaction_list)

        card_no = new_card_transaction_list[0].card_no

        balance_before_cancel = self.get_balances_by_card_no(card_no)

        balance_after_cancel = tuple(map(operator.add, balance_before_cancel, balance))

        # チャージ取消
        # 前払いバリュー残高はマイナスになってはいけない
        if new_transaction_type == 4 and balance_after_cancel[0] < 0:
            raise Exception('前払いバリュー残高がマイナスとなる')

        # 決済取消
        # 制限なし
        if new_transaction_type == 5:
            pass

        # ボーナス付与取消
        # 制限なし
        # ボーナスが利用されている場合、残高がマイナスになってもよい
        if new_transaction_type == 6:
            pass

        # ボーナス利用取消
        # 制限なし
        if new_transaction_type == 7:
            pass

        # ### CAUTION ###

        # ボーナスの有効期限超過、バリューの上限超過に関するチェックは、モデル定義後に実装する

        # ###############

        # 取り消される側の取引から新しい取引を作成する
        new_transaction = mock.MagicMock(
            # 新規のID
            id=str(uuid.uuid4()),
            # 新しく採番された取引番号
            transaction_id=new_transaction_id,
            # 現日時
            transaction_at=new_transaction_at,
            # 取消の取引種別
            transaction_type=new_transaction_type,
            # 取消を実行している店舗端末
            provider_id=terminal.provider_id,
            company_id=terminal.company_id,
            shop_id=terminal.shop_id,
            terminal_no=terminal.terminal_no,
            # 取消処理を適用後の残高合計(前払いバリュー、決済併用ボーナス、商品交換ボーナス)
            value_transaction_amount=balance_after_cancel[0],
            payable_bonus_transaction_amount=balance_after_cancel[1],
            product_exchange_bonus_amount=balance_after_cancel[2]
        )

        return_dict = {
            'cancel_target_transaction': cancel_target_transaction,
            'balance': balance,
            'balance_before_cancel': balance_before_cancel,
            'balance_after_cancel': balance_after_cancel,
            'new_transaction': new_transaction,
            'new_card_transactions': new_card_transaction_list
        }
        return return_dict

    def cancel_transaction(self, terminal, transaction_id, cancel_target_transaction_id):
        '''指定の取引を取り消す.

        Args:
            terminal (MagicMock型): 店舗端末.
            new_transaction_id (str型): 取消のために発行された新しい取引番号
            cancel_target_transaction_id (str型): 取り消される側の取引番号
        Returns:
            取消のカード取引リスト (list型):
        '''

        cancel_return = \
            self.create_cancel_transaction(terminal, transaction_id, cancel_target_transaction_id)

        self.save_new_transaction(
            cancel_return['cancel_target_transaction'],
            cancel_return['new_transaction'],
            cancel_return['new_card_transactions'])

        return self.make_response(
                cancel_return['cancel_target_transaction'].transaction_type,
                cancel_return['new_transaction'].transaction_at,
                terminal,
                cancel_return['balance'],
                cancel_return['balance_before_cancel'],
                cancel_return['balance_after_cancel'],
                cancel_return['new_card_transactions']
        )

    def save_new_transaction(self, cancel_target_transacion, new_transaction, new_card_transaction_list):
        '''取消の取引を保存する.

        Args:
            cancel_target_transaction (MagicMock型):
            new_transaction (MagicMock型): 取消の取引
            new_card_transaction_list (list型): 取消のカード取引のリスト
        Returns:
            取消のカード取引リスト (list型):
        '''

        cancel_target_transacion.cancel_id = new_transaction.id

        self.transaction_history.append(new_transaction)
        self.card_transaction_history.append(new_card_transaction_list)

    def make_response(self,
                      canceled_transaction_type,
                      cancel_at,
                      terminal,
                      balance,
                      balance_before_cancel,
                      balance_after_cancel,
                      new_card_transaction_list,
                      ):
        '''レスポンス用DTOを作成する.

        Args:
            canceled_transaction_type (int型): 取り消された側の取引種別
            cancel_at (datetime型): 取消日時
            terminal (MagicMock型): 店舗端末情報
            balance (tuple型): 取消処理の残高
            balance_before_cancel (tuple型): 取消処理前の残高
            balance_after_cancel (tuple型): 取消後の残高
            new_card_transaction_list (list型): 取消処理のカード取引リスト
        Returns:
            TransactionCancelResponse型: 取引取消のDTO
        '''

        company = TransactionCancelCompany(terminal.company_id, terminal.company_name)
        shop = TransactionCancelShop(terminal.shop_id, terminal.shop_name)

        total_amount = sum(balance)
        transaction_cancel = TransactionCancelTransaction(
            transaction_amount=total_amount,
            value_amount=balance[0],
            payable_bonus_amount=balance[1],
            product_exchange_amount=balance[2])
        balance_before_cancel = TransactionCancelBalance(
            value_balance=balance_before_cancel[0],
            value_expire_at=None,
            payable_bonus_balance=balance_before_cancel[1],
            product_exchange_bonus_balance=balance_before_cancel[2]
        )
        balance_after_cancel = TransactionCancelBalance(
            value_balance=balance_after_cancel[0],
            value_expire_at=None,
            payable_bonus_balance=balance_after_cancel[1],
            product_exchange_bonus_balance=balance_after_cancel[2]
        )

        # キャンペーンはリスト形式だが、モデル定義後に実装する。
        # ここでは空
        campaign = [
            TransactionCancelCampaign(
                event_name=None,
                cancel_grant_bank_account=0,
                cancel_grant_count=0,
                expire_at=None
            )
        ]

        card_no = new_card_transaction_list[0].card_no
        card = self.card_access_token_repository.get_card(card_no)

        card = [TransactionCancelCard(
            card_config_name=card.config_name,
            card_no=card.card_no,
            balance_before_cancel=balance_before_cancel,
            balance_after_cancel=balance_after_cancel,
            campaign=campaign)]

        return TransactionCancelResponse(
            canceled_transaction_type,
            cancel_at,
            company, shop,
            terminal.terminal_no,
            transaction_cancel,
            card
            )
