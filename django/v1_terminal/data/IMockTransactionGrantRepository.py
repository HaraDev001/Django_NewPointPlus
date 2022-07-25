from .ITransactionGrantRepository import ITransactionGrantRepository
from datetime import date, datetime, timezone, timedelta
from utils.datetime_utility import to_datetime, today
from unittest import mock

class IMockTransactionGrantRepository(ITransactionGrantRepository):
    '''
    ITransactionGrantRepositoryを実装したクラス

        ITransactionGrantRepositoryを実装したモックオブジェクトを扱うクラス

        Attributes:
            transactions (dict): 取引情報を保持
    '''

    def __init__(self):
        self.transactions = dict()
        JST = timezone(timedelta(hours=+9), 'JST')
        # 店舗情報
        shop_1 = mock.MagicMock(shop_number='888888', shop_name='shop_1')
        shop_2 = mock.MagicMock(shop_number='888888', shop_name='shop_2')

        # 企業情報
        company_1 = mock.MagicMock(company_number='999999', company_name='company_1')
        company_2 = mock.MagicMock(company_number='999999', company_name='company_2')

        campaign_1 = mock.MagicMock(campaign_name='テストイベント１', account_to_granted='99999999999', grant_amount=2000,
                                    usage_restriction_pattern=1,
                                    expired_at=datetime(2021 , 9 , 14 , 12 , 30, tzinfo=JST),
                                    grant_schedule_at=datetime(2021 , 8 , 14 , 12 , 30, tzinfo=JST))

        campaign_2 = mock.MagicMock(campaign_name='テストイベント２', account_to_granted='99999999999', grant_amount=2000,
                                    usage_restriction_pattern=1,
                                    expired_at=datetime(2021 , 9 , 14 , 12 , 30, tzinfo=JST),
                                    grant_schedule_at=datetime(2021 , 8 , 14 , 12 , 30, tzinfo=JST))

        value_transaction_balance=mock.MagicMock(
            total_balance=10000,
            usage_restriction_pattern=1,
            account_to_granted='999999'
        )
        payable_bonus_balance=mock.MagicMock(
            total_balance=10000,
            usage_restriction_pattern=1,
            account_to_granted='888888'
        )
        product_exchange_bonus_balance=mock.MagicMock(
            total_balance=10000,
            usage_restriction_pattern=1,
            account_to_granted='777777'
        )

        transaction_1 = mock.MagicMock(transaction_type=2, transaction_at=datetime(2021 , 7 , 4 , 12 , 30, tzinfo=JST),
                                        transaction_status=1, transaction_number='122345', shop=shop_1,
                                        company=company_1)

        transaction_2 = mock.MagicMock(transaction_type=1, transaction_at=datetime(2021 , 7 , 6 , 12 , 30, tzinfo=JST),
                                        transaction_status=1, transaction_number='122346', shop=shop_1,
                                        company=company_1)

        transaction_3 = mock.MagicMock(transaction_type=1, transaction_at=datetime(2021 , 7 , 4 , 12 , 30, tzinfo=JST),
                                        transaction_status=2, transaction_number='122345', shop=shop_1,
                                        company=company_1)

        transaction_4 = mock.MagicMock(transaction_type=2, transaction_at=datetime(2021 , 7 , 6 , 12 , 30, tzinfo=JST),
                                        transaction_status=1, transaction_number='122346', shop=shop_1,
                                        company=company_2)

        transaction_5 = mock.MagicMock(transaction_type=1, transaction_at=datetime(2021 , 7 , 3 , 12 , 30, tzinfo=JST),
                                        transaction_status=1, transaction_number='122347', shop=shop_1,
                                        company=company_2)

        transaction_6 = mock.MagicMock(transaction_type=2, transaction_at=datetime(2021 , 7 , 3 , 12 , 30, tzinfo=JST),
                                        transaction_status=2, transaction_number='122348', shop=shop_1,
                                        company=company_2)

        transaction_details_1 = mock.MagicMock(value_transaction_balance=value_transaction_balance,
                                                payable_bonus_balance=payable_bonus_balance,
                                                transaction=transaction_1,
                                                campaign=[campaign_1, campaign_2],
                                                card_no='9999999999990101',
                                                card_name='test',
                                                value_expired_at=datetime(2021 , 9 , 14 , 12 , 30, tzinfo=JST),
                                                product_exchange_bonus_balance=product_exchange_bonus_balance)

        transaction_details_2 = mock.MagicMock(value_transaction_balance=value_transaction_balance,
                                                payable_bonus_balance=payable_bonus_balance,
                                                transaction=transaction_1,
                                                campaign=[campaign_1, campaign_2],
                                                card_no='9999999999990102',
                                                card_name='test',
                                                value_expired_at=datetime(2021 , 9 , 14 , 12 , 30, tzinfo=JST),
                                                product_exchange_bonus_balance=product_exchange_bonus_balance)

        transaction_details_3 = mock.MagicMock(value_transaction_balance=value_transaction_balance,
                                                payable_bonus_balance=payable_bonus_balance,
                                                campaign=[campaign_1, campaign_2],
                                                transaction=transaction_1,
                                                card_no='9999999999990103',
                                                card_name='test',
                                                value_expired_at=datetime(2021 , 9 , 14 , 12 , 30, tzinfo=JST),
                                                product_exchange_bonus_balance=product_exchange_bonus_balance)

        transaction_details_4 = mock.MagicMock(value_transaction_balance=value_transaction_balance,
                                                transaction=transaction_1,
                                                campaign=[campaign_1, campaign_2],
                                                card_no='9999999999990104',
                                                card_name='test',
                                                payable_bonus_balance=payable_bonus_balance,
                                                value_expired_at=datetime(2021 , 9 , 14 , 12 , 30, tzinfo=JST),
                                                product_exchange_bonus_balance=product_exchange_bonus_balance)

        for transaction in [transaction_details_1, transaction_details_2, transaction_details_3, transaction_details_4]:
            key = transaction.card_no
            self.transactions[key] = transaction

    def grant(self, pk, card_no, terminal_no, amount, grant_method, grant_account, usage_restriction):
        '''
        ボーナス付与処理

        Attributes:
            pk(str)： 取引番号
            card_no(str): カード番号
            terminal_no(str): 端末番号
            amount(int): 付与額
            grant_method(int): 付与方法
            grant_account(str)： 付与口座
            usage_restriction(dict): 制限対象

        '''
        target_transaction = None
        for key, value in self.transactions.items():
            if card_no == key and value.transaction.transaction_number == pk:
                target_transaction = value

        #取引履歴テーブルのレコード作成がすでになされているか確認し、フェーズ2で実装
        #取引が紐づいた取引番号に対して異なる取引を行う場合エラーとなる。
        if not target_transaction:
            return None

        #ボーナスがマイナス状態の際、付与されるボーナスがマイナスとなっているボーナスと同じ利用制限を持つ
        #(もしくは利用制限が存在しない)場合はマイナス分の打ち消し処理を行う。
        bonus = target_transaction.payable_bonus_balance.total_balance
        bonus_usage_restriction_pattern = target_transaction.payable_bonus_balance.usage_restriction_pattern
        if usage_restriction['usage_restriction_pattern'] == bonus_usage_restriction_pattern and bonus < 0 \
            or not bonus_usage_restriction_pattern:
                    target_transaction.payable_bonus_balance.total_balance = bonus + amount


        payable_bonus_balance = target_transaction.payable_bonus_balance.total_balance
        product_exchange_bonus_balance = target_transaction.product_exchange_bonus_balance.total_balance
        if target_transaction.payable_bonus_balance.account_to_granted == grant_account:
            payable_bonus_balance = payable_bonus_balance + amount
        elif target_transaction.product_exchange_bonus_balance.account_to_granted == grant_account:
            product_exchange_bonus_balance = product_exchange_bonus_balance + amount


        transaction_after = mock.MagicMock(
            payable_bonus_balance=payable_bonus_balance,
            product_exchange_bonus_balance=product_exchange_bonus_balance)


        response_card_transaction = mock.MagicMock(
                card_no=target_transaction.card_no,
                card_name=target_transaction.card_name,
                transaction_before=mock.MagicMock(
                    payable_bonus_balance=target_transaction.payable_bonus_balance.total_balance,
                    product_exchange_bonus_balance=target_transaction.product_exchange_bonus_balance.total_balance
                ),
                transaction_after=transaction_after,
                campaign=target_transaction.campaign
            )

        response_grant = mock.MagicMock(
            amount=amount,
            grant_method=grant_method,
            grant_account= grant_account
        )

        response_transaction = mock.MagicMock(
            transaction_type=target_transaction.transaction.transaction_type,
            transaction_date=target_transaction.transaction.transaction_at,
            company=target_transaction.transaction.company,
            shop=target_transaction.transaction.shop,
            terminal_no=terminal_no,
            grant=response_grant,
            card_transaction=response_card_transaction
        )

        #保存
        for key, value in self.transactions.items():
            if card_no == key and value.transaction.transaction_number == pk:
                value = transaction_after
                break

        return response_transaction