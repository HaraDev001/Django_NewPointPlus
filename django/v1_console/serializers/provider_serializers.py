from database.models import Provider
from rest_framework import serializers


class ProviderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = "__all__"


class ProviderSerializer(serializers.ModelSerializer):
    provider_id = serializers.UUIDField(source="id")
    provider_owner_name = serializers.CharField(source="owner_name")
    use_service = serializers.SerializerMethodField()
    use_account = serializers.SerializerMethodField()
    use_web = serializers.SerializerMethodField()
    provider_status = serializers.IntegerField(source="status")

    class Meta:
        model = Provider
        fields = ["provider_id", "provider_name", "provider_status", "provider_owner_name", "use_service",
                  "use_account", "use_web"]

    def get_use_service(self, obj):
        return {
            "is_physical_card_enable": obj.physical_card_flag
        }

    def get_use_account(self, obj):
        return {
            "is_value_enable": obj.value_enabled_flag,
            "is_payable_bonus_enable": obj.payable_bonus_flag,
            "is_exchange_bonus_enable": obj.exchange_bonus_flag
        }

    def get_use_web(self, obj):
        return {
            "balance_inquiry_page_enable": obj.balance_inquiry_page_flag
        }
