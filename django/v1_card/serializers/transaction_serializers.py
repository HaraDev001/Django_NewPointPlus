from rest_framework import serializers, status
from ..buisiness_logic.transaction.transaction import Transaction
from ..buisiness_logic.transaction.transaction_list import TransactionList
from ..data.IMockAccessTokenRepository import IMockAccessTokenRepository
from ..data.ITransactionRepository import ITransactionRepository
from ..data.IDLTransactionRepository import IDLTransactionRepository


class TransactionDateRequestSerializer(serializers.Serializer):
    # 取引取得開始日時
    transaction_start = serializers.DateField(
        format="%Y-%m-%d",
        input_formats=["%Y-%m-%d"])
    # 取引取得終了日時
    transaction_end = serializers.DateField(
        format="%Y-%m-%d",
        input_formats=["%Y-%m-%d"])


class SearchSerializer(serializers.Serializer):
    # 取引種別
    transaction_type = serializers.IntegerField()
    # 取引取得日時
    transaction_date = TransactionDateRequestSerializer()
    # 取引状態
    transaction_status = serializers.IntegerField()


class TransactionSerializer(serializers.Serializer):
    # 取引額
    transaction_total_amount = serializers.FloatField()
    # 前払バリュー増減額
    transaction_value_amount = serializers.FloatField()
    # 決済併用ボーナス増減数
    transaction_payable_bonus_amount = serializers.FloatField()
    # 商品交換ボーナス増減数
    transaction_exchange_bonus_amount = serializers.FloatField()


class CampaignSerializer(serializers.Serializer):
    # 付与対象口座
    account_to_granted = serializers.CharField()
    # 付与数
    grant_amount = serializers.IntegerField()
    # 有効期限日
    expired_at = serializers.DateTimeField()
    # 付与予定日
    grant_schedule_at = serializers.DateTimeField()


class CardReplaceSerializer(serializers.Serializer):
    # 付替元カード設定名
    replace_source_card_setting_name = serializers.CharField()


class TransactionResponseSerializer(serializers.Serializer):
    # 取引種別
    transaction_type = serializers.IntegerField()
    # 取引日時
    transaction_at = serializers.DateTimeField()
    # 取引番号
    transaction_number = serializers.CharField()
    # 取引状態
    transaction_status = serializers.IntegerField()
    # 取引
    transaction = TransactionSerializer()
    # キャンペーン
    campaign = CampaignSerializer()
    # カード付替
    card_replace = CardReplaceSerializer()


class TransactionRequestSerializer(serializers.Serializer):
    # トークン
    access_token = serializers.CharField(required=True)
    # カード番号
    card_no = serializers.CharField(required=True)
    # 取引番号
    transaction_id = serializers.CharField(required=True)

    def create(self, validated_data):
        access_repository: IAccessTokenRepository = IMockAccessTokenRepository()
        transaction_repository: ITransactionRepository = IDLTransactionRepository()
        transaction = Transaction(access_repository, transaction_repository)
        instance, response_status = transaction.execute(
            validated_data['card_no'],
            validated_data['transaction_id'],
            validated_data['access_token'])
        if response_status == status.HTTP_200_OK:
            serializer = TransactionResponseSerializer(instance)
            return serializer.data, response_status
        else:
            return None, response_status


class TransactionListRequestSerializer(serializers.Serializer):
    # トークン
    access_token = serializers.CharField(required=True)
    # カード番号
    card_no = serializers.CharField(required=True)
    # 開始位置
    start_index = serializers.IntegerField(required=False)
    # 取得件数
    item_number = serializers.IntegerField(required=False)
    # 検索
    search = SearchSerializer()
    # 並び順
    sort_order = serializers.CharField(required=False)

    def create(self, validated_data):
        access_repository: IAccessTokenRepository = IMockAccessTokenRepository()
        transaction_repository: ITransactionRepository = IDLTransactionRepository()
        transaction_list = TransactionList(access_repository, transaction_repository)
        instance_list, response_status = transaction_list.execute(
            validated_data['card_no'],
            validated_data['access_token'],
            validated_data['search'])
        if response_status == status.HTTP_200_OK:
            response_list = []
            for instance in instance_list:
                responseserializer = TransactionResponseSerializer(instance)
                response_list.append(responseserializer.data)

            response_list = self.transaction_repository.execute_sort(
                serialize_list, validated_data['start_index'],
                validated_data['item_number'],
                validated_data['sort_order'])
        else:
            return None, response_status
