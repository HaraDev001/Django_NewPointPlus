from database.models import Company
from rest_framework import serializers
from v1_console.serializers import ManagementTagSerializer


class CompanyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"

    def create(self, validated_data):
        company = Company(
            company_name=validated_data['company_name'],
        )
        company.save()
        return company


class CompanySerializer(serializers.ModelSerializer):
    management_tags = ManagementTagSerializer(many=True)
    company_status = serializers.IntegerField(source="status")

    class Meta:
        model = Company
        fields = ['corporate_number', 'company_name', 'company_status', 'management_tags',  'remarks', ]
