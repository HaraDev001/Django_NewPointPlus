from rest_framework import serializers, status
from ..buisiness_logic.corp_info.corp_info import CorpInfo
from ..data.ICorpInfoRepository import ICorpInfoRepository
from ..data.IDLCorpInfoRepository import IDLCorpInfoRepository


class ServiceSerializer(serializers.Serializer):
    # 電子マネーカード可否
    e_money_card = serializers.IntegerField()


class AccountSerializer(serializers.Serializer):
    # 前払バリュー可否
    prepaid_value = serializers.IntegerField()
    # 決済併用ボーナス可否
    combined_bonus = serializers.IntegerField()
    # 商品交換ボーナス可否
    exchange_bonus = serializers.IntegerField()


class CorpInfoResponseSerializer(serializers.Serializer):
    # 事業者名
    company_name = serializers.CharField()
    # サービス名
    service_name = serializers.CharField()
    # 事業者サービスロゴURL
    logo_url = serializers.URLField()
    # 利用規約URL
    terms_of_service_url = serializers.URLField()
    # 利用規約規定日
    terms_of_service_regulation_date = serializers.DateTimeField()
    # 利用規約バージョン
    terms_of_service_version = serializers.CharField()
    # プライバシーポリシーURL
    privacy_policy_url = serializers.URLField()
    # プライバシーポリシー規定日
    privacy_policy_regulation_date = serializers.DateTimeField()
    # プライバシーポリシーバージョン
    privacy_policy_version = serializers.CharField()
    # 利用サービス
    service = ServiceSerializer()
    # 利用口座
    account = AccountSerializer(),
    # 著作権表示
    copyright_notice = serializers.CharField()


class CorpInfoRequestSerializer(serializers.Serializer):
    # header host
    host = serializers.CharField(required=True)

    def create(self, validated_data):
        corp_info_repository: ICorpInfoRepository = IDLCorpInfoRepository()
        corp_info = CorpInfo(corp_info_repository)
        instance, response_status = corp_info.execute(validated_data['host'])
        if response_status == status.HTTP_200_OK:
            serializer = CorpInfoResponseSerializer(instance)
            return serializer.data, response_status
        else:
            return None, response_status
