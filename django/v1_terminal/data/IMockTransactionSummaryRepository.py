from .ITransactionSummaryRepository import ITransactionSummaryRepository
from datetime import date, datetime, timezone, timedelta
from utils.datetime_utility import to_datetime, to_date
from unittest import mock

class IMockTransactionSummaryRepository(ITransactionSummaryRepository):
    '''
    ITransactionSummaryRepositoryを実装したクラス

        ITransactionSummaryRepositoryを実装したモックオブジェクトを扱うクラス

        Attributes:
            summary_infos (dict): 取引集計情報を保持
    '''

    def __init__(self):
        self.summary_infos = dict()
        JST = timezone(timedelta(hours=+9), 'JST')

        summary_info_1 = mock.MagicMock(
            terminal_no='terminal_01',
            aggregation_at=datetime(2021 , 7 , 4 , 12 , 30, tzinfo=JST),
            charge_total_amount=10000,
            charge_total_number=20,
            charge_cancal_total_amount=1000,
            charge_cancel_total_number=20,
            payment_total_amount=1000,
            payment_total_number=10,
            payment_cancal_total_amount=1000,
            payment_cancel_total_number=20,
            payment_prepaid_total_amount=4000,
            payment_prepaid_total_cancel_amount=4000,
            payment_payable_bonus_total_amount=3000,
            payment_payable_bonus_total_cancel_amount=3000,
            grant_payable_bonus_total_amount=4000,
            grant_payable_bonus_total_number=4000,
            grant_payable_bonus_total_cancel_amount=2000,
            grant_payable_bonus_cancel_total_number=3,
            grant_product_exchange_bonus_total_amount=2000,
            grant_product_exchange_bonus_total_number=13,
            grant_product_exchange_bonus_total_cancel_amount=2000,
            grant_product_exchange_bonus_cancel_total_number=12,
            use_product_exchange_bonus_total_amount=5000,
            use_product_exchange_bonus_total_number=2,
            use_product_exchange_bonus_total_cancel_amount=2000,
            use_product_exchange_bonus_cancel_total_number=10
        )

        summary_info_2 = mock.MagicMock(
            terminal_no='terminal_01',
            aggregation_at=datetime(2021 , 5 , 4 , 12 , 30, tzinfo=JST),
            charge_total_amount=10000,
            charge_total_number=20,
            charge_cancal_total_amount=1000,
            charge_cancel_total_number=20,
            payment_total_amount=1000,
            payment_total_number=10,
            payment_cancal_total_amount=1000,
            payment_cancel_total_number=20,
            payment_prepaid_total_amount=4000,
            payment_prepaid_total_cancel_amount=4000,
            payment_payable_bonus_total_amount=3000,
            payment_payable_bonus_total_cancel_amount=3000,
            grant_payable_bonus_total_amount=4000,
            grant_payable_bonus_total_number=4000,
            grant_payable_bonus_total_cancel_amount=2000,
            grant_payable_bonus_cancel_total_number=3,
            grant_product_exchange_bonus_total_amount=2000,
            grant_product_exchange_bonus_total_number=13,
            grant_product_exchange_bonus_total_cancel_amount=2000,
            grant_product_exchange_bonus_cancel_total_number=12,
            use_product_exchange_bonus_total_amount=5000,
            use_product_exchange_bonus_total_number=2,
            use_product_exchange_bonus_total_cancel_amount=2000,
            use_product_exchange_bonus_cancel_total_number=10
        )

        summary_info_3 = mock.MagicMock(
            terminal_no='terminal_02',
            aggregation_at=datetime(2021 , 7 , 4 , 12 , 30, tzinfo=JST),
            charge_total_amount=10000,
            charge_total_number=20,
            charge_cancal_total_amount=1000,
            charge_cancel_total_number=20,
            payment_total_amount=1000,
            payment_total_number=10,
            payment_cancal_total_amount=1000,
            payment_cancel_total_number=20,
            payment_prepaid_total_amount=4000,
            payment_prepaid_total_cancel_amount=4000,
            payment_payable_bonus_total_amount=3000,
            payment_payable_bonus_total_cancel_amount=3000,
            grant_payable_bonus_total_amount=4000,
            grant_payable_bonus_total_number=4000,
            grant_payable_bonus_total_cancel_amount=2000,
            grant_payable_bonus_cancel_total_number=3,
            grant_product_exchange_bonus_total_amount=2000,
            grant_product_exchange_bonus_total_number=13,
            grant_product_exchange_bonus_total_cancel_amount=2000,
            grant_product_exchange_bonus_cancel_total_number=12,
            use_product_exchange_bonus_total_amount=5000,
            use_product_exchange_bonus_total_number=2,
            use_product_exchange_bonus_total_cancel_amount=2000,
            use_product_exchange_bonus_cancel_total_number=10
        )



        for summary in [summary_info_1, summary_info_2, summary_info_3]:
            key = summary.aggregation_at
            self.summary_infos[key] = summary

    def summary(self, search):
        '''
        取引集計情報取得処理

        Attributes:
            terminal_no(str): 端末番号
            search(dict): 取引検索
        '''

        summary_list = []
        terminal_number = search['terminal_number']
        for key, value in self.summary_infos.items():
            if value.terminal_no == terminal_number:
                aggregation_at = to_date(value.aggregation_at)
                if not (aggregation_at >= search['search_date']['start_aggregation_at']) or \
                    not (aggregation_at <= search['search_date']['end_aggregation_at']):
                    continue
                summary_list.append(value)

        if len(summary_list) < 1:
            return None

        charge_total_amount = 0
        charge_total_number = 0

        charge_cancal_total_amount = 0
        charge_cancel_total_number = 0

        payment_total_amount = 0
        payment_total_number = 0

        payment_cancal_total_amount = 0
        payment_cancel_total_number = 0

        payment_prepaid_total_amount = 0
        payment_prepaid_total_cancel_amount = 0

        payment_payable_bonus_total_amount = 0
        payment_payable_bonus_total_cancel_amount = 0

        grant_payable_bonus_total_amount = 0
        grant_payable_bonus_total_number = 0

        grant_payable_bonus_total_cancel_amount = 0
        grant_payable_bonus_cancel_total_number = 0

        grant_product_exchange_bonus_total_amount = 0
        grant_product_exchange_bonus_total_number = 0

        grant_product_exchange_bonus_total_cancel_amount = 0
        grant_product_exchange_bonus_cancel_total_number = 0

        use_product_exchange_bonus_total_amount = 0
        use_product_exchange_bonus_total_number = 0

        use_product_exchange_bonus_total_cancel_amount = 0
        use_product_exchange_bonus_cancel_total_number = 0


        for summary in summary_list:
            charge_total_amount = charge_total_amount + summary.charge_total_amount
            charge_total_number = charge_total_number + summary.charge_total_number
            charge_cancal_total_amount = charge_cancal_total_amount + summary.charge_cancal_total_amount
            charge_cancel_total_number = charge_cancel_total_number + summary.charge_cancel_total_number
            payment_total_amount = payment_total_amount + summary.payment_total_amount
            payment_total_number = payment_total_number + summary.payment_total_number
            payment_cancal_total_amount = payment_cancal_total_amount + summary.payment_cancal_total_amount
            payment_cancel_total_number = payment_cancel_total_number + summary.payment_cancel_total_number
            payment_prepaid_total_amount = payment_prepaid_total_amount + summary.payment_prepaid_total_amount
            payment_prepaid_total_cancel_amount = \
                payment_prepaid_total_cancel_amount + summary.payment_prepaid_total_cancel_amount
            payment_payable_bonus_total_amount = \
                payment_payable_bonus_total_amount + summary.payment_payable_bonus_total_amount
            payment_payable_bonus_total_cancel_amount = \
                payment_payable_bonus_total_cancel_amount + summary.payment_payable_bonus_total_cancel_amount
            grant_payable_bonus_total_amount = \
                grant_payable_bonus_total_amount + summary.grant_payable_bonus_total_amount
            grant_payable_bonus_total_number = \
                grant_payable_bonus_total_number + summary.grant_payable_bonus_total_number
            grant_payable_bonus_total_cancel_amount = \
                grant_payable_bonus_total_cancel_amount + summary.grant_payable_bonus_total_cancel_amount
            grant_payable_bonus_cancel_total_number = \
                grant_payable_bonus_cancel_total_number + summary.grant_payable_bonus_cancel_total_number
            grant_product_exchange_bonus_total_amount = \
                grant_product_exchange_bonus_total_amount + summary.grant_product_exchange_bonus_total_amount
            grant_product_exchange_bonus_total_number = \
                grant_product_exchange_bonus_total_number + summary.grant_product_exchange_bonus_total_number
            grant_product_exchange_bonus_total_cancel_amount = \
                grant_product_exchange_bonus_total_cancel_amount + \
                    summary.grant_product_exchange_bonus_total_cancel_amount
            grant_product_exchange_bonus_cancel_total_number = \
                grant_product_exchange_bonus_total_cancel_amount + \
                    summary.grant_product_exchange_bonus_total_cancel_amount
            use_product_exchange_bonus_total_amount = \
                use_product_exchange_bonus_total_amount + summary.use_product_exchange_bonus_total_amount
            use_product_exchange_bonus_total_number = \
                use_product_exchange_bonus_total_number + summary.use_product_exchange_bonus_total_number


        response_charge = mock.MagicMock(
            total_amount=charge_total_amount,
            total_number=charge_total_number,
            cancal_total_amount=charge_cancal_total_amount,
            cancel_total_number=charge_cancel_total_number
        )

        response_prepaid_value_payment = mock.MagicMock(
            total_amount=payment_prepaid_total_amount,
            cancal_total_amount=payment_prepaid_total_cancel_amount,
        )

        response_payable_bonus_payment = mock.MagicMock(
            total_amount=payment_payable_bonus_total_amount,
            cancal_total_amount=payment_payable_bonus_total_cancel_amount,
        )

        response_payment = mock.MagicMock(
            total_amount=payment_total_amount,
            total_number=payment_total_number,
            cancal_total_amount=payment_cancal_total_amount,
            cancel_total_number=payment_cancel_total_number,
            prepaid_value=response_prepaid_value_payment,
            payable_bonus=response_payable_bonus_payment
        )

        response_payable_bonus_grant = mock.MagicMock(
            total_amount=grant_payable_bonus_total_amount,
            total_number=grant_payable_bonus_total_number,
            cancal_total_amount=grant_payable_bonus_total_cancel_amount,
            cancel_total_number=grant_payable_bonus_cancel_total_number,
        )

        response_product_exchange_bonus_grant = mock.MagicMock(
            total_amount=grant_product_exchange_bonus_total_amount,
            total_number=grant_product_exchange_bonus_total_number,
            cancal_total_amount=grant_product_exchange_bonus_total_cancel_amount,
            cancel_total_number=grant_product_exchange_bonus_cancel_total_number,
        )

        response_grant = mock.MagicMock(
            grant_payable_bonus=response_payable_bonus_grant,
            product_exchange_bonus=response_product_exchange_bonus_grant
        )

        response_product_exchange_bonus_use = mock.MagicMock(
            total_amount=use_product_exchange_bonus_total_amount,
            total_number=use_product_exchange_bonus_total_number,
            cancal_total_amount=use_product_exchange_bonus_total_cancel_amount,
            cancel_total_number=use_product_exchange_bonus_cancel_total_number,
        )

        response_use = mock.MagicMock(
            product_exchange_bonus=response_product_exchange_bonus_use
        )


        response_transaction = mock.MagicMock(
            charge=response_charge,
            payment=response_payment,
            grant=response_grant,
            use=response_use
        )

        return response_transaction

