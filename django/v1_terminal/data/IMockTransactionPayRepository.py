from .ITransactionPayRepository import ITransactionPayRepository
from datetime import date, datetime, timezone, timedelta
from utils.datetime_utility import to_datetime, today
from unittest import mock

class IMockTransactionPayRepository(ITransactionPayRepository):
    '''
    ITransactionPayRepositoryを実装したクラス

        ITransactionPayRepositoryを実装したモックオブジェクトを扱うクラス

        Attributes:
            transactions (dict): 取引情報を保持
    '''

    def __init__(self):
        self.transactions = dict()
        JST = timezone(timedelta(hours=+9), 'JST')
        # 店舗情報
        shop_1 = mock.MagicMock(shop_number=1, shop_name='shop_1')
        shop_2 = mock.MagicMock(shop_number=2, shop_name='shop_2')

        # 企業情報
        company_1 = mock.MagicMock(company_number=1, company_name='company_1')
        company_2 = mock.MagicMock(company_number=2, company_name='company_2')

        campaign_1 = mock.MagicMock(campaign_name='テストイベント１', account_to_granted='99999999999', grant_amount=2000,
                                    usage_limit_balance=1, expired_at=datetime(2021 , 9 , 14 , 12 , 30, tzinfo=JST),
                                    grant_schedule_at=datetime(2021 , 8 , 14 , 12 , 30, tzinfo=JST))

        campaign_2 = mock.MagicMock(campaign_name='テストイベント２', account_to_granted='99999999999', grant_amount=2000,
                                    usage_limit_balance=1, expired_at=datetime(2021 , 9 , 14 , 12 , 30, tzinfo=JST),
                                    grant_schedule_at=datetime(2021 , 8 , 14 , 12 , 30, tzinfo=JST))

        value_transaction_balance=mock.MagicMock(
            total_balance=10000,
            usage_limit_balance=1,
            account_to_granted='99999999999'
        )
        payable_bonus_balance=mock.MagicMock(
            total_balance=10000,
            usage_limit_balance=1,
            account_to_granted='99999999999'
        )
        product_exchange_bonus_balance=mock.MagicMock(
            total_balance=10000,
            usage_limit_balance=1,
            account_to_granted='99999999999'
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
            key = transaction.card_no + str(transaction.transaction.transaction_type)
            self.transactions[key] = transaction

    def pay(self, pk, card_info_list, terminal_no, payment_amount, campaign_flag):
        '''
        決済処理

        Attributes:
            pk(str)： 取引番号
            card_info_list(list): リクエストのカード情報
            card_no(str):　カード番号
            terminal_no(str): 端末番号
            payment_amount(int): 決済金額
            campaign_flag(dict): キャンペーン適用フラグ
        '''
        transaction_list = []
        target_transaction = None
        for card_info in card_info_list:
            for key, value in self.transactions.items():
                if card_info['card_no'] in key and value.transaction.transaction_number == pk:
                    transaction_list.append(value)
                    target_transaction = value.transaction

        if not target_transaction:
            return None
        #取引履歴テーブルのレコード作成がすでになされているか確認し、フェーズ2で実装
        #取引が紐づいた取引番号に対して異なる取引を行う場合エラーとなる。
        #取引種別 = 2は仮のデータ
        if target_transaction.transaction_type != 2:
            return None

        #非同期適用の場合、キャンペーン適用Batchへのリクエストを送信する必要があります。
        #後ほど実装
        #if campaign_flag.asynchronous == 1:
            #キャンペーン適用Batchへのリクエスト

        #ボーナスがマイナス状態の際、付与されるボーナスがマイナスとなっているボーナスと同じ利用制限を持つ
        #(もしくは利用制限が存在しない)場合はマイナス分の打ち消し処理を行う。
        bonus = target_transaction.transaction.payable_bonus_balance.total_balance
        campaign_bonus = target_transaction.campaign.usage_limit_balance
        bonus_usage_limit_balance = target_transaction.transaction.payable_bonus_balance.usage_limit_balance
        campaign_bonus_usage_limit_balance = target_transaction.campaign.usage_limit_balance
        if campaign_flag['sync'] == 1 and bonus < 0:
            if bonus_usage_limit_balance == campaign_bonus_usage_limit_balance or \
                not campaign_bonus_usage_limit_balance:
                    target_transaction.transaction.payable_bonus_balance.total_balance = bonus + campaign_bonus


        response_card_transaction_list = []

        #ボーナスの消費順序としては以下となります。
        #1. 有効期限が短いものから消費
        #2. 有効期限が同じ場合、利用制限があるものから消費
        #3. その他
        #mockは通常の方法で並び替えするのが困難であるためmodel定義後に実装

        remain = payment_amount
        used_payment_bonus_number = 0
        card_bonus_dict = dict()
        for transaction in transaction_list:
            if not transaction.card_no in card_bonus_dict:
                for card_info in card_info_list:
                    if card_info['card_no'] == transaction.card_no:
                        used_payment_bonus_number = card_info['used_payment_bonus']['used_payment_bonus_number']
                        card_bonus_dict[transaction.card_no] = used_payment_bonus_number

            value_remain = 0
            bonus_remain = \
            transaction.payable_bonus_balance.total_balance - card_bonus_dict[transaction.card_no]
            remain = remain - card_bonus_dict[transaction.card_no]

            if bonus_remain < 0:
                card_bonus_dict[transaction.card_no] = bonus_remain * -1
            else:
                card_bonus_dict[transaction.card_no] = 0

            value_remain = transaction.value_transaction_balance.total_balance - remain

            if value_remain < 0:
                remain = value_remain * -1
            else:
                remain = 0
            card_transaction = mock.MagicMock(
                card_no=transaction.card_no,
                card_name=transaction.card_name,
                transaction_before=mock.MagicMock(
                    value_expired_at=transaction.value_expired_at,
                    value_transaction_balance=\
                        transaction.value_transaction_balance.total_balance,
                    payable_bonus_balance=transaction.payable_bonus_balance.total_balance,
                    product_exchange_bonus_balance=transaction.payable_bonus_balance.total_balance

                ),
                transaction_after=mock.MagicMock(
                    value_expired_at=transaction.transaction.value_expired_at,
                    value_transaction_balance=0 if bonus_remain < 0 else bonus_remain,
                    payable_bonus_balance=0 if value_remain < 0 else value_remain,
                    product_exchange_bonus_balance=transaction.transaction.payable_bonus_balance.total_balance

                ),
                campaign=transaction.campaign
            )

            response_card_transaction_list.append(card_transaction)

        payable_bonus = 0
        for card_info in card_info_list:
            payable_bonus = payable_bonus + card_info['used_payment_bonus']['used_payment_bonus_number']

        response_payment = mock.MagicMock(
            payment_amount=payment_amount,
            prepaid_value = payment_amount - payable_bonus,
            payable_bonus = payable_bonus
        )


        response_transaction = mock.MagicMock(
            transaction_type=target_transaction.transaction_type,
            transaction_date=target_transaction.transaction_at,
            company=target_transaction.company,
            shop=target_transaction.shop,
            terminal_no=terminal_no,
            payment=response_payment,
            card_transaction=response_card_transaction_list
        )

        return response_transaction

