from rest_framework import serializers
from database.models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"

    def create(self, validated_data):
        company = Company(
            company_name=validated_data['company_name']
        )
        company.save()
        return company
