from rest_framework import serializers
from database.models import Card


class CardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = "__all__"

    def create(self, validated_data):
        card = Card(
        )
        card.save()
        return card


class CardDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = "__all__"

    def create(self, validated_data):
        card = Card(
        )
        card.save()
        return card


class CardListCsvSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = "__all__"

    def create(self, validated_data):
        card = Card(
        )
        card.save()
        return card
