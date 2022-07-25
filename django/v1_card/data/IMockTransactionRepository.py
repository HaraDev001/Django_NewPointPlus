from .ITransactionRepository import ITransactionRepository
from datetime import date, datetime, timezone, timedelta
from utils.datetime_utility import to_datetime, today
from unittest import mock


class IMockTransactionRepository(ITransactionRepository):
	def __init__(self):
		self.transactions = dict()
		JST = timezone(timedelta(hours=+9), 'JST')
		campaign = mock.MagicMock(account_to_granted='99999999999', grant_amount=2000,
                                    expired_at=datetime(2021 , 9 , 14 , 12 , 30, tzinfo=JST),
                                    grant_schedule_at=datetime(2021 , 8 , 14 , 12 , 30, tzinfo=JST))

		card_replace = mock.MagicMock(replace_source_card_setting_name='テスト１')

		transaction_details_1 = mock.MagicMock(transaction_amount=100000, transaction_value_amount=2000,
												transaction_payable_bonus_amount=100,
												transaction_exchange_bonus_amount=3000)
		transaction_details_2 = mock.MagicMock(transaction_amount=200000, transaction_value_amount=3000,
												transaction_payable_bonus_amount=100,
												transaction_exchange_bonus_amount=4000)
		transaction_details_3 = mock.MagicMock(transaction_amount=200000, transaction_value_amount=3000,
												transaction_payable_bonus_amount=100,
												transaction_exchange_bonus_amount=4000)
		transaction_details_4 = mock.MagicMock(transaction_amount=300000, transaction_value_amount=4000,
												transaction_payable_bonus_amount=100,
												transaction_exchange_bonus_amount=5000)

		transaction_1 = mock.MagicMock(card_no='9999999999990101', campaign=campaign, card_replace=card_replace,
										transaction_type=1, transaction_at=datetime(2021 , 7 , 4 , 12 , 30, tzinfo=JST),
										transaction_status=1, transaction_number='122345',
										transaction=transaction_details_1)
		transaction_2 = mock.MagicMock(card_no='9999999999990101', campaign=campaign, card_replace=card_replace,
										transaction_type=1, transaction_at=datetime(2021 , 7 , 6 , 12 , 30, tzinfo=JST),
										transaction_status=1, transaction_number='122346',
										transaction=transaction_details_2)
		transaction_3 = mock.MagicMock(card_no='9999999999990101', campaign=campaign, card_replace=card_replace,
										transaction_type=1, transaction_at=datetime(2021 , 7 , 4 , 12 , 30, tzinfo=JST),
										transaction_status=1, transaction_number='122345',
										transaction=transaction_details_1)
		transaction_4 = mock.MagicMock(card_no='9999999999990101', campaign=campaign, card_replace=card_replace,
										transaction_type=2, transaction_at=datetime(2021 , 7 , 6 , 12 , 30, tzinfo=JST),
										transaction_status=1, transaction_number='122346',
										transaction=transaction_details_2)
		transaction_5 = mock.MagicMock(card_no='9999999999990102', campaign=campaign,card_replace=None,
										transaction_type=1, transaction_at=datetime(2021 , 7 , 3 , 12 , 30, tzinfo=JST),
										transaction_status=1, transaction_number='122347',
										transaction=transaction_details_3)
		transaction_6 = mock.MagicMock(card_no='9999999999990103', campaign=campaign,card_replace=card_replace,
										transaction_type=2, transaction_at=datetime(2021 , 7 , 3 , 12 , 30, tzinfo=JST),
										transaction_status=2, transaction_number='122348',
										transaction=transaction_details_4)

		for transaction in [transaction_1, transaction_2, transaction_3, transaction_4, transaction_5, transaction_6]:
			key = transaction.card_no
			if key not in self.transactions:
				self.transactions[key] = [transaction]
			else:
				self.transactions[key].append(transaction)


	def get_transaction(self, card_number, transaction_id):
		'''取引履歴詳細情報を取得する.
            取引履歴詳細情報を取得する.
        Args:
            card_number (str型): カード番号.
			transaction_id (str型): 取引番号.
        Returns:
            取引履歴詳細情報: 指定されたカード番号、取引番号のモックオブジェクトがなければ、Noneを返却する.
        '''

		transaction_list = self.transactions.get(card_number, [])
		transaction = None
		for transaction_item in transaction_list:
			if transaction_item.transaction_number == transaction_id:
				transaction = transaction_item
				break
		return transaction


	def get_transaction_list(self, card_number, search):
		'''取引履歴一覧情報を取得する.
            取引履歴一覧情報を取得する.
        Args:
            card_number (str型): カード番号.
			search (dict型): 検索条件.
        Returns:
            取引履歴一覧情報: 指定されたカード番号,
			検索条件のモックオブジェクトがなければ、Noneを返却する.
        '''

		transaction_list = self.transactions.get(card_number, [])
		response_transaction = []
		for transaction in transaction_list:
			if transaction.transaction_type != search.get('transaction_type'):
				continue
			if transaction.transaction_status != search.get('transaction_status'):
				continue
			transaction_date = search.get('transaction_date')
			transaction_start = datetime.strptime(transaction_date.get('transaction_start'), '%Y-%m-%d')
			transaction_end = datetime.strptime(transaction_date.get('transaction_end'), '%Y-%m-%d')

			date_transaction_start = to_datetime(transaction_start)
			date_transaction_end = to_datetime(transaction_end)
			if transaction.transaction_at >= date_transaction_start and transaction.transaction_at <= date_transaction_end:
				response_transaction.append(transaction)
		return response_transaction