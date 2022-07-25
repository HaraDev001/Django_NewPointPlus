from database.models import Transaction
from database.models.transaction_category import TransactionCategory
from rest_framework import serializers


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"

    def create(self, validated_data):
        transaction = Transaction(
        )
        transaction.save()
        return transaction


class TransactionCancelRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"

    def create(self, validated_data):
        transaction = Transaction(
        )
        transaction.save()
        return transaction


class TransactionTypeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='transaction_category_name')

    class Meta:
        model = TransactionCategory
        fields = ['id', 'name']

    def create(self, validated_data):
        transaction = TransactionCategory(
        )
        transaction.save()
        return transaction


class TransactionTypeListSerializer(serializers.Serializer):
    transaction_types = TransactionTypeSerializer(many=True)


class TransactionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"

    def create(self, validated_data):
        transaction = Transaction(
        )
        transaction.save()
        return transaction


class TransactionListCsvSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"

    def create(self, validated_data):
        transaction = Transaction(
        )
        transaction.save()
        return transaction
