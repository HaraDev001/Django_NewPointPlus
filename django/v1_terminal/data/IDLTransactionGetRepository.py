from datetime import datetime, timedelta, timezone
from unittest import mock

from utils.datetime_utility import to_utc_timestamp

from .ITransactionGetRepository import ITransactionGetRepository
from database.models.shop import Shop
from database.models.company import Company
from database.models.transaction import Transaction
from database.models.terminal import Terminal
from database.models.campaign import Campaign
from database.models.apply_campaign import ApplyCampaign
from database.models.card import Card
from database.models.card_config import CardConfig
from database.models.bonus import Bonus
from database.models.use_condition import UseCondition
from database.models.transaction_category import TransactionCategory


class IMockTransactionGetRepository(ITransactionGetRepository):
    '''
    ITransactionGetRespositoryを実装したクラス

        ITransactionGetRepositoryを実装したモックオブジェクトを扱うクラス

        Attributes:
            transactions_for_detail (dict): 取引履歴詳細取得のための取引履歴情報を保持
            transactions_for_list (dict): 取引履歴一覧取得のための取引履歴情報を保持
            terminal_authorizations (dict): 店舗端末認証情報を保持
            cards (dict): カード情報を保持
    '''
    def __init__(self):
        self.transactions_for_list = dict()
        self.transactions_for_detail = dict()
        self.terminal_authorizations = dict()
        self.cards = dict()

        JST = timezone(timedelta(hours=+9), 'JST')
        transaction_contents = Transaction.objects.all()
        transaction_details_array=[]
        campaignDataArray = []
        cardDataArray=[]
        card_in_transaction_array=[]
        card_merge_array=[]
        transaction_array=[]
        for transaction_content in transaction_contents:
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
            terminalId = transaction_content.terminal_id
            terminalConent = Terminal.objects.get(id=terminalId)
            terminalInfo = {
                'terminal_number': terminalConent.terminal_number,
                'terminal_name': terminalConent.terminal_name
            }
            consumerId = transaction_content.consumer_id
            cardDatas = Card.objects.get(consumer_id=consumerId)
            bonusData = Bonus.objects.get(card_id=cardData.id)
            useConditionData = UseCondition.objects.get(id=bonusData.use_condition_id)
            apply_campaign_ids = transaction_content.apply_campaign_ids
            apply_campaign_ids = transaction_content.apply_campaign_ids
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
                for cardData in cardDatas:
                    cardNumber = cardData.card_number
                    cardConfigData = CardConfig.objects.get(id=cardData.card_config_id)
                    card_in_transaction_1 = mock.MagicMock(
                        card_config_name=cardConfigData.name,
                        card_no=cardNumber,
                        campaign=[campaignDataItem]
                    )
                    card_in_transaction_array.append(card_in_transaction_1)
                    cardDataArray.append(card_in_transaction_1)
                    if cardData.status=0:
                        merge_source = mock.MagicMock(
                            card_config_name=cardConfigData.name,
                            card_no=cardNumber
                        )
                    else:
                        merge_target = mock.MagicMock(
                            card_config_name=cardConfigData.name,
                            card_no=cardNumber
                        )
                    card_merge = {
                        'merge_source':merge_source,
                        'merge_target':merge_target
                        }
                    card_merge_array.append(card_merge)     

            transaction_details_1 = {
                'transaction_amount':transaction_content.amount, 
                'value_transaction_fluctuate_amount':transaction_content.total_prepaid_value_amount,
                'payable_bonus_fluctuate_amount':transaction_content.total_payable_bonus_amount,
                'product_exchange_bonus_fluctuate_amount':transaction_content.total_exchange_bonus_amount
            }
            transaction_details_array.append(transaction_details_1)
            transactionCategory=TransactionCategory.objects.get(id=transaction_content.category)
            # フェーズ1ではMock内に必要な情報のすべてを持っている前提で設定する。
            # モデル定義後書き換える。
            transaction_1 = {
                magnetic_information=transaction_content.magnetic_information,
                card_merge=card_merge_array,
                card=card_in_transaction_array,
                transaction_type= transactionCategory.name,
                transaction_at=transaction_content.transaction_at,
                transaction_status=transaction_content.status, 
                transaction_number=transaction_content.transaction_number,
                transaction=transaction_details_1,
                company=company_1,
                shop=shop_1,
                terminal=terminal_1
            }
            transaction_array.append(transaction_1)
        # 取引履歴一覧取得のための取引履歴は端末番号ごとにリストに格納する。
        for transaction in transaction_array:
            key = transaction.terminal.terminal_no
            if key not in self.transactions_for_list:
                self.transactions_for_list[key] = [transaction]
            else:
                self.transactions_for_list[key].append(transaction)

        # 取引履歴詳細取得のための取引履歴は取引番号をキーに辞書に格納する。
        for transaction_for_detail in transaction_details_array:
            key = transaction_for_detail.transaction_number
            self.transactions_for_detail[key] = transaction_for_detail

        # 店舗端末認証情報
        terminal_authorization_1 = mock.MagicMock(
            terminal_no='1',
            access_token='header.payload.terminal_1',
            access_token_expires_at=to_utc_timestamp(
                datetime(2025, 7, 31, 12, 0, 0))
        )
        terminal_authorization_2 = mock.MagicMock(
            terminal_no='2',
            access_token='header.payload.terminal_2',
            access_token_expires_at=to_utc_timestamp(
                datetime(2021, 7, 1, 12, 0, 0))
        )
        for terminal_authorization in [
            terminal_authorization_1, terminal_authorization_2,
        ]:
            key = terminal_authorization.access_token
            self.terminal_authorizations[key] = terminal_authorization

        card_101 = mock.MagicMock(
            card_no='9999999999990101', card_pin='0101', state=1,
            payment=True, service_user_policy=True,
            provider_id='110000001', company_user_policy=True)
        card_102 = mock.MagicMock(
            card_no='9999999999990102', card_pin='0102', state=2,
            payment=True, service_user_policy=False,
            provider_id='110000001', company_user_policy=True)
        card_103 = mock.MagicMock(
            card_no='9999999999990103', card_pin='0103', state=1,
            payment=True, service_user_policy=True,
            provider_id='110000001', company_user_policy=True)

        for card in [card_101, card_102, card_103]:
            key = card.card_no
            self.cards[key] = card

    def get_card(self, card_number):
        '''カード情報を取得する.

            カード情報を取得する.

        Args:
            card_no (str型): カード番号.

        Returns:
            カード情報: 指定されたカード番号のモックオブジェクトがなければ、例外を発生させる.

        Raises:
            Exception: リクエストされたカード番号＆PINで一致するカードがない

        '''
        key = card_number
        try:
            card = self.cards[key]
        except KeyError:
            raise Exception('リクエストされたカード番号で一致するカードがない')
        return card

    def get_terminal_authorization(self, terminal_access_token):
        '''店舗端末認証情報を取得する.

            認証トークン及び端末番号に一致するカードを取得する

        Args:
            terminal_access_token (str型): 認証トークン
            terminal_no (str型): 端末番号

        Returns:
            店舗端末認証情報: 指定された認証トークンに一致するモックオブジェクトがなければ、例外を発生させる.

        Raises:
            Exception: リクエストされた認証トークンと端末番号で一致する店舗端末認証情報がない
            Exception: リクエストされた認証トークンで一致する店舗端末認証情報がない

        '''

        key = terminal_access_token
        try:
            terminal_authorization = self.terminal_authorizations[key]
        except KeyError:
            raise Exception('リクエストされた認証トークンで一致する店舗端末認証情報がない')
        return terminal_authorization

    def get_transaction_list(
        self, authorization_terminal_no, transaction_type, transaction_start, transaction_end, transaction_status,
        terminal_no, card_no, magnetic_information
    ):
        '''取引履歴一覧情報を取得する.
            取引履歴一覧情報を取得する.
        Args:
            authorization_terminal_no (str): 認証トークンから取得した端末番号
            transaction_type (int): リクエストから取得した取引種別
            transaction_start (DateTime): リクエストから取得した取引日時（From）
            transaction_end (DateTime): リクエストから取得した取引日時（To）
            transaction_status (int): リクエストから取得した取引ステータス
            terminal_no (str): リクエストから取得した端末番号
            card_no (str):  リクエストから取得したカード番号
            magnetic_information (str): リクエストから取得した磁気情報

        Returns:
            取引履歴一覧情報: 指定された検索条件、端末番号のオブジェクトがなければ、空のリストを返却する。
        '''

        # 端末番号での抽出
        transaction_list = self.transactions_for_list.get(authorization_terminal_no, [])
        response_transaction = []
        for transaction in transaction_list:
            # search_criteria内の各項目は、定義されていないこともある。
            # 各parameterの値がNoneの場合は、抽出に使用しない。
            # 取引種別での抽出
            if transaction_type and transaction.transaction_type != transaction_type:
                continue
            # 取引ステータスでの抽出
            if transaction_status and transaction.transaction_status != transaction_status:
                continue
            # 端末番号での抽出
            if terminal_no and transaction.terminal.terminal_no != terminal_no:
                continue
            # 磁気情報での抽出
            if magnetic_information and transaction.magnetic_information != magnetic_information:
                continue
            # カード番号での抽出
            if card_no:
                card_flag = False
                for card_data in transaction.card:
                    if card_data.card_no == card_no:
                        card_flag = True
                        break
                if not card_flag:
                    continue

            # 開始日時と終了日時からの抽出
            # どちらも設定されている。
            if transaction_start and transaction_end:
                if transaction_start <= transaction.transaction_at <= transaction_end:
                    response_transaction.append(transaction)
            # 開始日時のみ設定されている。
            elif transaction_start and not transaction_end:
                if transaction_start <= transaction.transaction_at:
                    response_transaction.append(transaction)
            # 終了日時のみ設定されている。
            elif not transaction_start and transaction_end:
                if transaction.transaction_at <= transaction_end:
                    response_transaction.append(transaction)
            # どちらも設定されていない。
            else:
                response_transaction.append(transaction)

        return response_transaction

    def get_transaction(self, transaction_number):
        '''取引履歴詳細情報を取得する.
            取引履歴詳細情報を取得する.
        Args:
            transaction_id (int型): 取引番号.
        Returns:
            取引履歴詳細情報: 指定されたカード番号、取引番号のモックオブジェクトがなければ、Noneを返却する.
        '''
        key = transaction_number
        try:
            transaction = self.transactions_for_detail[key]
        except KeyError:
            raise Exception('リクエストされた取引番号で一致する取引履歴がない')
        return transaction
