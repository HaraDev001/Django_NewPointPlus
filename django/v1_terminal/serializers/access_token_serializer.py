from rest_framework import serializers

from v1_terminal.data.ITerminalAccessTokenRepository import ITerminalAccessTokenRepository
from v1_terminal.data.IMockTerminalAccessTokenRepository import IMockTerminalAccessTokenRepository

from v1_terminal.buisiness_logic.access_token.issue_access_token import (
    IssueAccessToken
)
from v1_terminal.buisiness_logic.access_token.update_access_token import (
    UpdateAccessToken
)
from v1_terminal.buisiness_logic.access_token.invalidate_access_token import (
    InvalidateAccessToken
)


class AccessTokenIssueRequestSerializer(serializers.Serializer):
    mail_address = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    terminal_no = serializers.CharField(required=True)

    def create(self, validated_data):
        repository: ITerminalAccessTokenRepository = IMockTerminalAccessTokenRepository()
        issue_access_token = IssueAccessToken(repository)

        access_token_response, status = issue_access_token.execute(
            **validated_data)
        return access_token_response, status


class AccessTokenIssueResponseSerializer(serializers.Serializer):
    access_token = serializers.CharField(required=True)
    access_token_expire_at = serializers.IntegerField(required=True)
    refresh_token = serializers.CharField(required=True)


class AccessTokenUpdateRequestSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)

    def create(self, validated_data):
        refresh_token = validated_data['refresh_token']
        repository: ITerminalAccessTokenRepository = IMockTerminalAccessTokenRepository()
        update_access_token = UpdateAccessToken(repository)

        access_token_response, status = update_access_token.execute(
            refresh_token)
        return access_token_response, status


class AccessTokenDeleteRequestSerializer(serializers.Serializer):
    access_token = serializers.CharField(required=True)
    refresh_token = serializers.CharField(required=True)

    def create(self, validated_data):
        access_token = validated_data['access_token']
        refresh_token = validated_data['refresh_token']
        repository: ITerminalAccessTokenRepository = IMockTerminalAccessTokenRepository()
        invalidate_access_token = InvalidateAccessToken(repository)

        status = invalidate_access_token.execute(
            access_token, refresh_token)
        return status
