from .ITransactionChargeRepository import ITransactionChargeRepository
from datetime import date, datetime, timezone, timedelta
from utils.datetime_utility import to_datetime, today
from unittest import mock


class IMockTransactionChargeRepository(ITransactionChargeRepository):
    '''
    ITransactionChargeRepositoryを実装したクラス

        ITransactionChargeRepositoryを実装したモックオブジェクトを扱うクラス

        Attributes:
            cards (dict): カード情報を保持
            terminal_authorizations (dict): 店舗端末認証情報を保持
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

        campaign = mock.MagicMock(campaign_name='テストイベント', account_to_granted='99999999999', grant_amount=2000,
                                    usage_limit_balance=1, expired_at=datetime(2021 , 9 , 14 , 12 , 30, tzinfo=JST),
                                    grant_schedule_at=datetime(2021 , 8 , 14 , 12 , 30, tzinfo=JST))

        value_transaction_balance=mock.MagicMock(
            total_balance=1000,
            usage_limit_balance=1,
            account_to_granted='99999999999'
        )
        payable_bonus_balance=mock.MagicMock(
            total_balance=1000,
            usage_limit_balance=1,
            account_to_granted='99999999999'
        )
        product_exchange_bonus_balance=mock.MagicMock(
            total_balance=1000,
            usage_limit_balance=1,
            account_to_granted='99999999999'
        )

        transaction_details_1 = mock.MagicMock(value_transaction_balance=value_transaction_balance,
												payable_bonus_balance=payable_bonus_balance,
                                                value_expired_at=datetime(2021 , 9 , 14 , 12 , 30, tzinfo=JST),
												product_exchange_bonus_balance=product_exchange_bonus_balance)

        transaction_details_2 = mock.MagicMock(value_transaction_balance=value_transaction_balance,
												payable_bonus_balance=payable_bonus_balance,
                                                value_expired_at=datetime(2021 , 9 , 14 , 12 , 30, tzinfo=JST),
												product_exchange_bonus_balance=product_exchange_bonus_balance)

        transaction_details_3 = mock.MagicMock(value_transaction_balance=value_transaction_balance,
												payable_bonus_balance=payable_bonus_balance,
                                                value_expired_at=datetime(2021 , 9 , 14 , 12 , 30, tzinfo=JST),
												product_exchange_bonus_balance=product_exchange_bonus_balance)

        transaction_details_4 = mock.MagicMock(value_transaction_balance=value_transaction_balance,
												payable_bonus_balance=payable_bonus_balance,
                                                value_expired_at=datetime(2021 , 9 , 14 , 12 , 30, tzinfo=JST),
												product_exchange_bonus_balance=product_exchange_bonus_balance)

        transaction_1 = mock.MagicMock(card_no='9999999999990101', campaign=campaign,
										transaction_type=1, transaction_at=datetime(2021 , 7 , 4 , 12 , 30, tzinfo=JST),
										transaction_status=1, transaction_number='122345', shop=shop_1,
										company=company_1, transaction=transaction_details_1)

        transaction_2 = mock.MagicMock(card_no='9999999999990101', campaign=campaign,
										transaction_type=1, transaction_at=datetime(2021 , 7 , 6 , 12 , 30, tzinfo=JST),
										transaction_status=1, transaction_number='122346', shop=shop_1,
										company=company_1, transaction=transaction_details_2)

        transaction_3 = mock.MagicMock(card_no='9999999999990101', campaign=campaign,
										transaction_type=1, transaction_at=datetime(2021 , 7 , 4 , 12 , 30, tzinfo=JST),
										transaction_status=1, transaction_number='122345', shop=shop_1,
										company=company_1, transaction=transaction_details_1)

        transaction_4 = mock.MagicMock(card_no='9999999999990101', campaign=campaign,
										transaction_type=2, transaction_at=datetime(2021 , 7 , 6 , 12 , 30, tzinfo=JST),
										transaction_status=1, transaction_number='122346', shop=shop_1,
										company=company_2, transaction=transaction_details_2)

        transaction_5 = mock.MagicMock(card_no='9999999999990102', campaign=campaign,
										transaction_type=1, transaction_at=datetime(2021 , 7 , 3 , 12 , 30, tzinfo=JST),
										transaction_status=1, transaction_number='122347', shop=shop_1,
										company=company_2, transaction=transaction_details_3)

        transaction_6 = mock.MagicMock(card_no='9999999999990103', campaign=campaign,
										transaction_type=1, transaction_at=datetime(2021 , 7 , 3 , 12 , 30, tzinfo=JST),
										transaction_status=2, transaction_number='122348', shop=shop_1,
                                        company=company_2, transaction=transaction_details_4)

        for transaction in [transaction_1, transaction_2, transaction_3, transaction_4, transaction_5, transaction_6]:
            key = transaction.card_no

            if key not in self.transactions:
                self.transactions[key] = [transaction]
            else:
                self.transactions[key].append(transaction)

    def charge(self, pk, card_no, principal_id, charge_amount, campaign_flag):
        '''
        チャージ処理

        Attributes:
            pk(str)： 取引番号
            access_token(str): 認証トークン
            card_no(str):　カード番号
            charge_amount(int): チャージ金額
            campaign_flag(dict): キャンペーン適用フラグ
        '''
        transaction_list = self.transactions[card_no]
        target_transaction = None
        for transaction in transaction_list:
            if transaction.transaction_number == pk:
                target_transaction = transaction
                break
        if not target_transaction:
            return None
        #取引履歴テーブルのレコード作成がすでになされているか確認し、フェーズ2で実装
        #取引が紐づいた取引番号に対して異なる取引を行う場合エラーとなる。
        #取引種別 = 1は仮のデータ
        if target_transaction.transaction_type != 1:
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

        #対象口座の取得ロジックは仮のもの(フェーズ2にて実装予定)
        response_charge = mock.MagicMock(
            target_account=target_transaction.transaction.value_transaction_balance.account_to_granted,
            charge_amount=charge_amount
        )

        transaction_after = mock.MagicMock(
            value_expired_at=target_transaction.transaction.value_expired_at,
            value_transaction_balance=\
            target_transaction.transaction.value_transaction_balance.total_balance + charge_amount,
            payable_bonus_balance=target_transaction.transaction.payable_bonus_balance,
            product_exchange_bonus_balance=target_transaction.transaction.payable_bonus_balance
        )


        #カードに設定されているであろうカード設定名取得ロジックはフェーズ2で実装予定
        response_card_transaction = mock.MagicMock(
            card_no=card_no,
            card_name='テスト1',
            transaction_before=mock.MagicMock(
                value_expired_at=target_transaction.transaction.value_expired_at,
                value_transaction_balance=\
                target_transaction.transaction.value_transaction_balance.total_balance,
                payable_bonus_balance=target_transaction.transaction.payable_bonus_balance.total_balance,
                product_exchange_bonus_balance=target_transaction.transaction.payable_bonus_balance.total_balance

            ),
            transaction_after=transaction_after
        )

        response_transaction = mock.MagicMock(
            transaction_type=target_transaction.transaction_type,
            transaction_date=target_transaction.transaction_at,
            company=target_transaction.company,
            shop=target_transaction.shop,
            terminal_no=principal_id,
            charge=response_charge,
            card_transaction=response_card_transaction
        )

        #保存
        transaction_list = self.transactions[card_no]
        for transaction in transaction_list:
            if transaction.transaction_number == pk:
                transaction = transaction_after
                break

        return response_transaction



