import datetime
import os

from config.test_base import BaseTestCase
from database.models import Provider
from rest_framework.test import APITestCase


class ProviderAPICase(BaseTestCase):
    api_name = "Api Provider List"
    path_to_folder = os.path.abspath(os.path.dirname(__file__)) + "/testcase/providers"

    def setUp(self):
        Provider.objects.create(id="1e7ac16e213b45d0ac0eb26072f7f5c2", status=0, owner_name="test1",
                                owner_phonetic_name="test1", owner_address_pref="te",
                                owner_address_city="test1", owner_address_town="te",
                                owner_birthday=datetime.date.today(), provider_name="test1",
                                provider_postal_code="test1", provider_address_pref="te",
                                provider_address_city="test1", provider_phone_number="test1",
                                start_available_date=datetime.date.today())
        Provider.objects.create(id="c259a03047304ccc96193e15f6e4da58", status=0, owner_name="test2",
                                owner_phonetic_name="test2", owner_address_pref="te",
                                owner_address_city="test2", owner_address_town="te",
                                owner_birthday=datetime.date.today(), provider_name="test2",
                                provider_postal_code="test2", provider_address_pref="te",
                                provider_address_city="test2", provider_phone_number="test2",
                                start_available_date=datetime.date.today())
        super(ProviderAPICase, self).setUp()


class ProviderTestAuthentication(APITestCase):
    def test_provider_list_not_authentication(self):
        url = "/console/api/v1/providers/"
        request = self.client.get(url)
        self.assertEqual(request.status_code, 401)
