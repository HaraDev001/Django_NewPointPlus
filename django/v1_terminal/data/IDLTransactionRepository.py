
from .ITransactionRepository import ITransactionRepository
from datetime import date, datetime, timezone, timedelta
from utils.datetime_utility import to_datetime, today
from database.models.transaction import Transaction
from database.models.campaign import Campaign
from database.models.card import Card
from database.models.card_config import CardConfig

class IDLTransactionRepository(ITransactionRepository):

    def set_transaction_response(self, transaction_data):
        '''取引情報をレスポンスに整形する.
            Args:
                transaction_data (Transaction型): 取引情報.
            Returns:
            取引情報.
        '''

        apply_campaign_ids = transaction_data.apply_campaign_ids
        campaign_datas = []
        for apply_campaign_id in apply_campaign_ids:
            campaign_datas.append(Campaign.objects.get(id=apply_campaign_id))
        campaign_list = []
        for campaign_data in campaign_datas:
            campaign = {
                'account_to_granted': campaign_data.account_to_granted,
                'grant_amount': campaign_data.grant_amount,
                'start_at': campaign_data.start_campaign_at,
                'expired_at': campaign_data.end_campaign_at
            }
            campaign_list.append(campaign)
        card_replace = {
            'replace_source_card_setting_name': transaction_data.replace_source_card_setting_name
            }

        transaction_details = {
            'transaction_total_amount': transaction_data.transaction_total_amount,
            'transaction_value_amount': transaction_data.transaction_value_amount,
            'transaction_payable_bonus_amount': transaction_data.transaction_payable_bonus_amount,
            'transaction_exchange_bonus_amount': transaction_data.transaction_exchange_bonus_amount
        }

        transaction = {
            'card_no':transaction_data.card,
            'campaign':campaign_list,
            'card_replace':card_replace,
            'transaction_type':transaction_data.transaction_type,
            "transaction_at" : transaction_data.transaction_at,
            "transaction_status" : transaction_data.transaction_status,
            "transaction_number" : transaction_data.transaction_number,
            "transaction" : transaction_details
        }
        return transaction


    def get_transaction(self, card_number, transaction_id):
        '''取引履歴詳細情報を取得する.
            Args:
                card_number (str型): カード番号.
                transaction_id (str型): 取引番号.
            Returns:
            取引履歴詳細情報: 指定されたカード番号、取引番号のモックオブジェクトがなければ、Noneを返却する.
        '''

        transaction_data = Transaction.objects.get(id=transaction_id, card=card_number)
        transaction = self.set_transaction_response(transaction_data)
        return transaction


    def get_transaction_list(self, card_number, search):
        '''取引履歴一覧情報を取得する.
            Args:
                card_number (str型): カード番号.
                search (dict型): 検索条件.
            Returns:
                取引履歴一覧情報: 指定されたカード番号,
                検索条件のモックオブジェクトがなければ、Noneを返却する.
        '''

        transaction_list = Transaction.objects.filter(card=card_number).all()
        response_transaction = []
        for transaction_data in transaction_list:
            transaction = self.set_transaction_response(transaction_data)
            if transaction.transaction_type != search.get('transaction_type'):
                continue
            if transaction.transaction_status != search.get('transaction_status'):
                continue
            transaction_date = search.get('transaction_date')
            transaction_start = datetime.strptime(transaction_date.get('transaction_start'), '%Y-%m-%d')
            transaction_end = datetime.strptime(transaction_date.get('transaction_end'), '%Y-%m-%d')

            date_transaction_start = to_datetime(transaction_start)
            date_transaction_end = to_datetime(transaction_end)
            if transaction.transaction_at >= date_transaction_start and \
                transaction.transaction_at <= date_transaction_end:
                response_transaction.append(transaction)


        return response_transaction
