from .ITransactionChargeRepository import ITransactionChargeRepository
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
        response_charge = {
            'target_account':target_transaction.transaction.value_transaction_balance.account_to_granted,
            'charge_amount':charge_amount
        }

        transaction_after = {
            'value_expired_at':target_transaction.transaction.value_expired_at,
            'value_transaction_balance':\
            target_transaction.transaction.value_transaction_balance.total_balance + charge_amount,
            'payable_bonus_balance':target_transaction.transaction.payable_bonus_balance,
            'product_exchange_bonus_balance':target_transaction.transaction.payable_bonus_balance
        }


        #カードに設定されているであろうカード設定名取得ロジックはフェーズ2で実装予定
        response_card_transaction = {
            'card_no':card_no,
            'card_name':target_transaction.card_name,
            'transaction_before':{
                'value_expired_at':target_transaction.transaction.value_expired_at,
                'value_transaction_balance':\
                target_transaction.transaction.value_transaction_balance.total_balance,
                'payable_bonus_balance':target_transaction.transaction.payable_bonus_balance.total_balance,
                'product_exchange_bonus_balance':target_transaction.transaction.payable_bonus_balance.total_balance

            },
            'transaction_after':transaction_after
        )

        response_transaction = {
            'transaction_type':target_transaction.transaction_type,
            'transaction_date':target_transaction.transaction_at,
            'company':target_transaction.company,
            'shop':target_transaction.shop,
            'terminal_no':principal_id,
            'charge':response_charge,
            'card_transaction':response_card_transaction
        }

        #保存
        transaction_list = self.transactions[card_no]
        for transaction in transaction_list:
            if transaction.transaction_number == pk:
                transaction = transaction_after
                break

        return response_transaction



