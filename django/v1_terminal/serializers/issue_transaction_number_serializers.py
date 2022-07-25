from rest_framework import serializers, status
from v1_terminal.buisiness_logic.transaction.issue_transaction_number import \
    IssueTransactionNumber
from v1_terminal.data.IIssueTransactionNumberReposiotry import \
    IIssueTransactionNumberRepository
from v1_terminal.data.IMockIssueTransactionNumberRepository import \
    IMockIssueTransactionnNumberRepository


class IssueTransactionNumberRequestSerializer(serializers.Serializer):

    access_token = serializers.CharField(required=True)

    def create(self, validated_data):
        terminal_access_token = validated_data['access_token']

        repository: IIssueTransactionNumberRepository =\
            IMockIssueTransactionnNumberRepository()
        issue_transaction_number = IssueTransactionNumber(repository)

        instance, response_status = issue_transaction_number.execute(
            terminal_access_token)
        if response_status == status.HTTP_200_OK:
            serializer = IssueTransactionNumberResponseSerializer(instance)
            return serializer.data, response_status
        else:
            return None, response_status


class IssueTransactionNumberResponseSerializer(serializers.Serializer):

    transaction_number = serializers.CharField(required=True)
