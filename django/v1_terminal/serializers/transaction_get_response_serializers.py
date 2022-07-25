from rest_framework import serializers


class CompanySerializer(serializers.Serializer):

    company_number = serializers.IntegerField()
    company_name = serializers.CharField()


class ShopSerializer(serializers.Serializer):

    shop_number = serializers.IntegerField()
    shop_name = serializers.CharField()


class TerminalSerializer(serializers.Serializer):

    terminal_no = serializers.CharField()


class TransactionSerializer(serializers.Serializer):
    # 取引額
    transaction_amount = serializers.IntegerField()
    # 前払バリュー増減額
    value_transaction_fluctuate_amount = serializers.IntegerField()
    # 決済併用ボーナス増減数
    payable_bonus_fluctuate_amount = serializers.IntegerField()
    # 商品交換ボーナス増減数
    product_exchange_bonus_fluctuate_amount = serializers.IntegerField()


class CampaignSerializer(serializers.Serializer):
    # 付与対象口座
    account_to_granted = serializers.CharField()
    # 付与数
    grant_amount = serializers.IntegerField()


class CardSerializer(serializers.Serializer):
    # カード設定名
    card_config_name = serializers.CharField()
    # カード番号
    card_no = serializers.CharField()
    # キャンペーン
    campaign = CampaignSerializer(many=True)


class MergeCardSerializer(serializers.Serializer):

    card_config_name = serializers.CharField()
    card_no = serializers.CharField()


class CardMergeSerializer(serializers.Serializer):

    merge_source = MergeCardSerializer()
    merge_target = MergeCardSerializer()


class TransactionResponseSerializer(serializers.Serializer):
    # 取引種別
    transaction_type = serializers.IntegerField()
    # 取引日時
    transaction_at = serializers.DateTimeField()
    # 取引番号
    transaction_number = serializers.IntegerField()
    # 取引状態
    transaction_status = serializers.CharField()
    # 企業
    company = CompanySerializer()
    # 店舗
    shop = ShopSerializer()
    # 端末
    terminal = TerminalSerializer()
    # 取引
    transaction = TransactionSerializer()
    # カード
    card = CardSerializer(many=True)
    # カード付替
    card_merge = CardMergeSerializer()


class TransactionResponseListSerializer(serializers.Serializer):

    transaction_history = TransactionResponseSerializer(many=True)
