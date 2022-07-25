from rest_framework import serializers
from database.models import Transaction


class CardTransactionSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"

    def create(self, validated_data):
        transaction = Transaction(
        )
        transaction.save()
        return transaction


class BalanceSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"

    def create(self, validated_data):
        transaction = Transaction(
        )
        transaction.save()
        return transaction


class EventSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"

    def create(self, validated_data):
        transaction = Transaction(
        )
        transaction.save()
        return transaction


class CardIssueTotalSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"

    def create(self, validated_data):
        transaction = Transaction(
        )
        transaction.save()
        return transaction


class CardIssueTransitionSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"

    def create(self, validated_data):
        transaction = Transaction(
        )
        transaction.save()
        return transaction
