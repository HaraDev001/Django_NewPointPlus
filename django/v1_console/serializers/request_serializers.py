from rest_framework import serializers
from database.models import Transaction


class RequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = "__all__"

    def create(self, validated_data):
        transaction = Transaction(
        )
        transaction.save()
        return transaction


class CancelRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"

    def create(self, validated_data):
        transaction = Transaction(
        )
        transaction.save()
        return transaction


class RequestListSerializer(serializers.Serializer):
    requests = RequestSerializer(many=True)
