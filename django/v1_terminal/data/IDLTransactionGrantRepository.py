from .ITransactionGrantRepository import ITransactionGrantRepository
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

class IMockTransactionGrantRepository(ITransactionGrantRepository):
    '''
    ITransactionGrantRepositoryを実装したクラス

        ITransactionGrantRepositoryを実装したモックオブジェクトを扱うクラス

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
            'total_balance':transaction_content.total_exchange_bonus_amount,
            'usage_restriction_pattern':useConditionData.category,
            'account_to_granted':bonusData.grant_count
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

        product_exchange_bonus_balance={
            'total_balance':cardConfigData.total_balance,
            'usage_limit_balance':cardConfigData.exchange_bonus_balance_limit,
            'account_to_granted':cardConfigData.account_to_granted
        }

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
        key = transaction_details_1.card_no
        self.transactions[key] = transaction_details_1

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


        transaction_after = {
            'payable_bonus_balance':payable_bonus_balance,
            'product_exchange_bonus_balance':product_exchange_bonus_balance}


        response_card_transaction = {
                'card_no':target_transaction.card_no,
                'card_name':target_transaction.card_name,
                'transaction_before': {
                    'payable_bonus_balance':target_transaction.payable_bonus_balance.total_balance,
                    'product_exchange_bonus_balance':target_transaction.product_exchange_bonus_balance.total_balance
                },
                'transaction_after':transaction_after,
                'campaign':target_transaction.campaign
        }

        response_grant = {
            'amount':amount,
            'grant_method':grant_method,
            'grant_account':grant_account
        }

        response_transaction = {
            'transaction_type':target_transaction.transaction.transaction_type,
            'transaction_date':target_transaction.transaction.transaction_at,
            'company':target_transaction.transaction.company,
            'shop':target_transaction.transaction.shop,
            'terminal_no':terminal_no,
            'grant':response_grant,
            'card_transaction':response_card_transaction
        }

        #保存
        for key, value in self.transactions.items():
            if card_no == key and value.transaction.transaction_number == pk:
                value = transaction_after
                break

        return response_transaction