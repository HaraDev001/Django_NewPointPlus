from rest_framework import serializers
from database.models import Shop


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = "__all__"

    def create(self, validated_data):
        shop = Shop(
            shop_name=validated_data['shop_name'],
        )
        shop.save()
        return shop


class ShopListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = "__all__"

    def create(self, validated_data):
        shop = Shop(
            company_name=validated_data['shop_name'],
        )
        shop.save()
        return shop
