
from rest_framework import serializers


class AuthIssueTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    login_password = serializers.CharField(max_length=255)
    send_email_flag = serializers.BooleanField()


class AuthUpdateTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=2000)


class AuthRevokeTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=2000)
