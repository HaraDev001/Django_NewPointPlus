from .ITransactionPayRepository import ITransactionPayRepository
from datetime import date, datetime, timezone, timedelta
from utils.datetime_utility import to_datetime, today
from unittest import mock
from database.models.shop import Shop
from database.models.company import Company
from database.models.transaction import Transaction
from database.models.campaign import Campaign
from database.models.apply_campaign import ApplyCampaign
from database.models.card import Card
from database.models.card_config import CardConfig
from database.models.bonus import Bonus
from database.models.use_condition import UseCondition

class IDLTransactionPayRepository(ITransactionPayRepository):
    '''
    ITransactionPayRepositoryを実装したクラス

        ITransactionPayRepositoryを実装したモックオブジェクトを扱うクラス

        Attributes:
            transactions (dict): 取引情報を保持
    '''

    def __init__(self, transactionId):
        self.transactions = dict()
        JST = timezone(timedelta(hours=+9), 'JST')
        # 店舗情報
        transaction_content = Transaction.objects.get(id=transactionId)
        shopId = transaction_content.shop_id
        shopContent = Shop.objects.get(id=shopId)
        shopInfo = {
            'shop_number': shopContent.shop_number,
            'shop_name': shopContent.shop_name
        }
        # 企業情報
        companyId = transaction_content.company_id
        companyConent = Company.objects.get(id=companyId)
        companyInfo = {
            'company_number': companyConent.company_number,
            'company_name': companyConent.company_name
        }
        consumerId = transaction_content.consumer_id
        cardData = Card.objects.get(consumer_id=consumerId)
        cardNumber = cardData.card_number
        cardConfigData = CardConfig.objects.get(id=cardData.card_config_id)
        bonusData = Bonus.objects.get(card_id=cardData.id)
        useConditionData = UseCondition.objects.get(id=bonusData.use_condition_id)
        value_transaction_balance={
            'total_balance': transaction_content.total_prepaid_value_amount,
            'usage_restriction_pattern':useConditionData.category,
            'account_to_granted':bonusData.grant_count
        }
        payable_bonus_balance={
            'total_balance':transaction_content.total_payable_bonus_amount,
            'usage_restriction_pattern':useConditionData.category,
            'account_to_granted':bonusData.grant_count
        }
        product_exchange_bonus_balance={
            'total_balance':cardConfigData.total_balance,
            'usage_limit_balance':cardConfigData.exchange_bonus_balance_limit,
            'account_to_granted':cardConfigData.account_to_granted
        }
        apply_campaign_ids = transaction_content.apply_campaign_ids
        campaignDataArray = []
        for campaignId in apply_campaign_ids:
            campaignData = Campaign.objects.get(id=campaignId)
            applyCampaignData = ApplyCampaign.objects.get(campaign_id=campaignData.id)
            campaignDataItem = {
                'campaign_name': campaignData.campaign_name,
                'account_to_granted' : applyCampaignData.account_to_granted,
                'grant_amount': applyCampaignData.bonus_grant_count,
                'usage_limit_balance': applyCampaignData.usage_limit_balance,
                'expired_at': applyCampaignData.bonus_expired_at,
                'grant_schedule_at': applyCampaignData.applied_at
            }
            campaignDataArray.append(campaignDataItem)
        

        transaction_1 = {
            'transaction_type':transaction_content.category, 
            'transaction_at':transaction_content.transaction_at,
            'transaction_status':transaction_content.status,
            'transaction_number':transaction_content.transaction_number, 
            'shop':shopInfo,
            'company':companyInfo
        }
        transaction_details_1 = {
            'transaction':transaction_1,
            'campaign':campaignDataArray,
            'card_no':cardNumber,
            'card_name':cardConfigData.card_name,
            'value_transaction_balance':value_transaction_balance,
            'payable_bonus_balance':payable_bonus_balance,
            'product_exchange_bonus_balance':product_exchange_bonus_balance
        }
        key = transaction_details_1.card_no + str(transaction_details_1.transaction.transaction_type)
        self.transactions[key] = transaction_details_1

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
            card_transaction = {
                'card_no': transaction.card_no,
                'card_name':transaction.card_name,
                'transaction_before':{
                    'value_expired_at':transaction.value_expired_at,
                    'value_transaction_balance':\
                        transaction.value_transaction_balance.total_balance,
                    'payable_bonus_balance':transaction.payable_bonus_balance.total_balance,
                    'product_exchange_bonus_balance':transaction.payable_bonus_balance.total_balance
                },
                'transaction_after':{
                    'value_expired_at':transaction.transaction.value_expired_at,
                    'value_transaction_balance':0 if bonus_remain < 0 else bonus_remain,
                    'payable_bonus_balance':0 if value_remain < 0 else value_remain,
                    'product_exchange_bonus_balance':transaction.transaction.payable_bonus_balance.total_balance

                },
                'campaign':transaction.campaign
            }

            response_card_transaction_list.append(card_transaction)

        payable_bonus = 0
        for card_info in card_info_list:
            payable_bonus = payable_bonus + card_info['used_payment_bonus']['used_payment_bonus_number']

        response_payment = {
            'payment_amount':payment_amount,
            'prepaid_value' : payment_amount - payable_bonus,
            'payable_bonus' : payable_bonus
        }


        response_transaction = {
            'transaction_type':target_transaction.transaction_type,
            'transaction_date':target_transaction.transaction_at,
            'company':target_transaction.company,
            'shop':target_transaction.shop,
            'terminal_no':terminal_no,
            'payment':response_payment,
            'card_transaction':response_card_transaction_list
        }

        return response_transaction

