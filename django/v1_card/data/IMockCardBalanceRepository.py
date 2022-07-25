from datetime import date
from unittest import mock

from .ICardBalanceRepository import ICardBalanceRepository


class IMockCardBalanceRepository(ICardBalanceRepository):
    '''
    ICardBalanceRepositoryを実装したクラス

        ICardBalanceReposiotryを実装したモックオブジェクトを扱うクラス

        Attributes:
            card_balances(dict): カード残高情報を保持
    '''

    def __init__(self):
        self.card_balances = dict()
        # 店舗情報
        shop_1 = mock.MagicMock(shop_number=1, shop_name='shop_1')
        shop_2 = mock.MagicMock(shop_number=2, shop_name='shop_2')

        # 企業情報
        company_1 = mock.MagicMock(company_number=1, company_name='company_1')
        company_2 = mock.MagicMock(company_number=2, company_name='company_2')

        # 制限対象
        usage_limit_target_1 = mock.MagicMock(
            shop=[shop_1, shop_2], company=[company_1, company_2])
        usage_limit_target_2 = mock.MagicMock(
            shop=[shop_1], company=[company_1])

        # balance_type = (暫定)0: 前払いバリュー, 1: 決済併用ボーナス, 2: 商品交換ボーナス
        card_balance_101_1 = mock.MagicMock(
            card_no='9999999999990101',
            balance_id='1',
            balance=10_000,
            balance_type=0,
            expires_at=date(2023, 7, 30),
            usage_limit_target=usage_limit_target_1,
            usage_limit_id='1',
            to_be_granted=False,
            to_be_granted_at=None
        )
        card_balance_101_2 = mock.MagicMock(
            card_no='9999999999990101',
            balance_id='2',
            balance=10_000,
            balance_type=0,
            expires_at=date(2023, 7, 31),
            usage_limit_target=usage_limit_target_2,
            usage_limit_id='2',
            to_be_granted=False,
            to_be_granted_at=None
        )
        card_balance_101_3 = mock.MagicMock(
            card_no='9999999999990101',
            balance_id='3',
            balance=10_000,
            balance_type=0,
            expires_at=date(2023, 7, 31),
            usage_limit_target=usage_limit_target_1,
            usage_limit_id='1',
            to_be_granted=True,
            to_be_granted_at=date(2022, 1, 1)
        )
        card_balance_101_4 = mock.MagicMock(
            card_no='9999999999990101',
            balance_id='4',
            balance=15_000,
            balance_type=1,
            expires_at=date(2023, 7, 30),
            usage_limit_target=usage_limit_target_1,
            usage_limit_id='1',
            to_be_granted=False,
            to_be_granted_at=None
        )
        card_balance_101_5 = mock.MagicMock(
            card_no='9999999999990101',
            balance_id='5',
            balance=15_000,
            balance_type=1,
            expires_at=date(2023, 7, 31),
            usage_limit_target=usage_limit_target_2,
            usage_limit_id='2',
            to_be_granted=False,
            to_be_granted_at=None
        )
        card_balance_101_6 = mock.MagicMock(
            card_no='9999999999990101',
            balance_id='6',
            balance=15_000,
            balance_type=1,
            expires_at=date(2023, 7, 30),
            usage_limit_target=usage_limit_target_1,
            usage_limit_id='1',
            to_be_granted=True,
            to_be_granted_at=date(2022, 1, 1)
        )
        card_balance_101_7 = mock.MagicMock(
            card_no='9999999999990101',
            balance_id='7',
            balance=20_000,
            balance_type=2,
            expires_at=date(2023, 7, 30),
            usage_limit_target=usage_limit_target_1,
            usage_limit_id='1',
            to_be_granted=False,
            to_be_granted_at=None
        )
        card_balance_101_8 = mock.MagicMock(
            card_no='9999999999990101',
            balance_id='8',
            balance=20_000,
            balance_type=2,
            expires_at=date(2023, 7, 31),
            usage_limit_target=usage_limit_target_2,
            usage_limit_id='2',
            to_be_granted=False,
            to_be_granted_at=None
        )
        card_balance_101_9 = mock.MagicMock(
            card_no='9999999999990101',
            balance_id='9',
            balance=20_000,
            balance_type=2,
            expires_at=date(2023, 7, 30),
            usage_limit_target=usage_limit_target_1,
            usage_limit_id='1',
            to_be_granted=True,
            to_be_granted_at=date(2022, 1, 1)
        )

        for card_balance in [
                card_balance_101_1, card_balance_101_2, card_balance_101_3,
                card_balance_101_4, card_balance_101_5, card_balance_101_6,
                card_balance_101_7, card_balance_101_8, card_balance_101_9
                ]:
            key = card_balance.card_no + str(card_balance.balance_type) +\
                card_balance.balance_id
            self.card_balances[key] = card_balance

    def get_card_balance_by_type(self, card_no, balance_type):
        '''balance_typeに応じたカード残高を取得、集計する。

            各種残高の集計処理はフェーズ1では実装しない。

        Args:
            card_no(str型): カード番号
            balance_type(int型): カード残高種別
                                (暫定)0: 前払いバリュー, 1: 決済併用ボーナス, 2: 商品交換ボーナス

        Returns
            カード残高情報: 指定されたbalance_typeの残高情報のみ集計して返却する。

        '''
        target_key = card_no + str(balance_type)
        target_records = []
        for key, value in self.card_balances.items():
            if target_key in key:
                target_records.append(value)

        balances_by_usage_limit = []
        balances_by_expiration = []
        to_be_granted_balances = []
        total_balance = 0
        for record in target_records:
            # total_balanceの集計
            total_balance += record.balance
            # 付与予定残高でない
            if not record.to_be_granted_at:
                # フェーズ１では各残高の集計処理はせず、単純に1レコードずつリストに追加する。
                # 利用制限別残高
                balance_by_usage_limit = mock.MagicMock(
                    usage_limit_pattern=record.usage_limit_id,
                    target=record.usage_limit_target,
                    balance=record.balance
                    )
                balances_by_usage_limit.append(balance_by_usage_limit)
                # 有効期限別残高
                balance_by_expiration = mock.MagicMock(
                    expires_at=record.expires_at,
                    balance=record.balance
                )
                balances_by_expiration.append(balance_by_expiration)

            else:
                # 付与予定残高
                to_be_granted_balance = mock.MagicMock(
                    to_be_granted_at=record.to_be_granted_at,
                    balance=record.balance
                )
                to_be_granted_balances.append(to_be_granted_balance)

        return mock.MagicMock(
            total_balance=total_balance,
            balance_by_usage_limit=balances_by_usage_limit,
            balance_by_expiration=balances_by_expiration,
            to_be_granted_balance=to_be_granted_balances
        )
