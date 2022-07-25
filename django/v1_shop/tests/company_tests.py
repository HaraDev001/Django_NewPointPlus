import json

from django.test import TestCase

# from database.models import Company


class CompanyTests(TestCase):
    # def test_post_success(self):
    #     url = 'http://localhost:8000/shop/api/v1/companies/'
    #     data = {  # FIXME: Need update parameter: provider
    #         'company_name': 'テスト'
    #     }
    #
    #     response = self.client.post(url, json.dumps(data), content_type='application/json')
    #     results = json.loads(response.content)
    #
    #     self.assertEqual(results['status']['code'], 200)
    #     self.assertEqual(Company.objects.count(), 1)
    #     self.assertEqual(Company.objects.get().company_name, data['company_name'])

    def test_post_fail(self):
        url = 'http://localhost:8000/shop/api/v1/companies/'
        data = {
            'company_name': True
        }

        response = self.client.post(url, json.dumps(data), content_type='application/json')
        results = json.loads(response.content)

        self.assertEqual(results['status']['code'], 500)
