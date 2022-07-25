from database.models import PermissionManagement
from rest_framework import serializers


class OperationPermissionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionManagement
        fields = ['permission_id', 'permission_name', 'permission_content', 'remarks']

    permission_id = serializers.UUIDField(source='permission.id')
    permission_name = serializers.CharField(source='permission.name')
    permission_content = serializers.SerializerMethodField()

    def get_permission_content(self, instance):
        return {
            "target": instance.permission.target,
            "permission": instance.state
        }


class InitializePwdRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    login_password = serializers.CharField(max_length=255)
    session = serializers.CharField(max_length=2048)  # max_length reference: https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_RespondToAuthChallenge.html  # noqa: E501
