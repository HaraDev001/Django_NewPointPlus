from rest_framework.views import APIView
from rest_framework.response import Response


class AccountingHistoryRerieveView(APIView):

    def get(self, request, pk, *args, **kwargs):
        return Response({
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
        })
