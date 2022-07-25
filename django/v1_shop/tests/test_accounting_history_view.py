from rest_framework.test import APITestCase
from rest_framework import status


class AccountingHistoryViewTests(APITestCase):
    '''会計履歴詳細APIのテストクラス'''

    maxDiff = None
    TARGET_URL = '/shop/api/v1/accounting_history/{}/'

    def test_get_retrive_success(self):
        '''正常系'''

        expected_json_dict = {
            'status': {
                'code': 200,
                'message': '',
            },
            'info': {
                'date': '',
                'info': {
                    'accounting_id': '',
                    'cancel_status': 0,
                    'total_grant_amount': 0,
                    'total_payment_amount': 0,
                },
                'card': {
                    'card_id': '',
                    'card_config_name': '',
                },
                'operation_info': {
                    'shop_id': '',
                    'terminal_id': '',
                },
                'detail': {
                    'request_id': '',
                    'receipt_id': '',
                    'transactions': [
                        '',
                    ],
                },
            },
        }

        response = self.client.get(self.TARGET_URL.format('aaaa'))
        # ステータスコードの検証
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # JSONの検証
        self.assertJSONEqual(response.content, expected_json_dict)
