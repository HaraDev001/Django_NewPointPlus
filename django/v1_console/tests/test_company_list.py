import datetime
import os

from config.test_base import BaseTestCase
from database.models import Company, ManagementTag, Provider
from database.models.common.choices import ManagementTagCategory
from rest_framework.test import APITestCase


class CompanyAPICase(BaseTestCase):
    api_name = "Api Company List"
    path_to_folder = os.path.abspath(os.path.dirname(__file__)) + "/testcase/company"

    def setUp(self):
        provider1 = Provider.objects.create(id="1e7ac16e213b45d0ac0eb26072f7f5c2",
                                            owner_name="test1",
                                            owner_phonetic_name="test1", owner_address_pref="te",
                                            owner_address_city="test1", owner_address_town="te",
                                            owner_birthday=datetime.date.today(), provider_name="test1",
                                            provider_postal_code="test1", provider_address_pref="te",
                                            provider_address_city="test1", provider_phone_number="test1",
                                            start_available_date=datetime.date.today())
        provider2 = Provider.objects.create(id="c259a03047304ccc96193e15f6e4da58", owner_name="test2",
                                            owner_phonetic_name="test2", owner_address_pref="te",
                                            owner_address_city="test2", owner_address_town="te",
                                            owner_birthday=datetime.date.today(), provider_name="test2",
                                            provider_postal_code="test2", provider_address_pref="te",
                                            provider_address_city="test2", provider_phone_number="test2",
                                            start_available_date=datetime.date.today())
        tag1 = ManagementTag.objects.create(name="tag1", category=ManagementTagCategory.COMPANY)
        tag2 = ManagementTag.objects.create(name="tag2", category=ManagementTagCategory.COMPANY)
        company1 = Company.objects.create(id="4c92a2e9-27c3-41aa-844f-352fbebfdefa", provider=provider1,
                                          corporate_number="656416",
                                          company_name="test2", status=2, postal_code="24", address_pref="13",
                                          remarks="remark2",
                                          address_city="124", address_town="124",
                                          address_other="124", phone_number="6595498", available_service="4",
                                          available_transaction_type="23fq", start_available_date=datetime.date.today())
        company2 = Company.objects.create(
            id="46bd8be2-406f-4140-a97a-1a76d75be6ca", provider=provider2, corporate_number="68498494",
            company_name="test1", status=1, postal_code="341", address_pref="12", remarks="remark1", address_city="413",
            address_town="412", address_other="1413", phone_number="14414", available_service="4353",
            available_transaction_type="32rhaa", start_available_date=datetime.date.today())
        company1.management_tags.add(tag1)
        company2.management_tags.add(tag1, tag2)

        super(CompanyAPICase, self).setUp()


class ProviderTestAuthentication(APITestCase):
    def test_provider_list_not_authentication(self):
        url = "/console/api/v1/companies/"
        request = self.client.get(url)
        self.assertEqual(request.status_code, 401)
