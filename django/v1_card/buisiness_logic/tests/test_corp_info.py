from unittest import mock
from rest_framework import status
from django.test import SimpleTestCase
from v1_card.data.ICorpInfoRepository import ICorpInfoRepository
from v1_card.data.IMockCorpInfoRepository import IMockCorpInfoRepository
from v1_card.buisiness_logic.corp_info.corp_info import CorpInfo

class CorpInfoTests(SimpleTestCase):

    # フェーズ2でテスト項目を増やす
    # hostあり
    def test_get_corp_info_101_success(self):
        request_data = 'localhost:8000'
        corp_info_repository: ICorpInfoRepository = IMockCorpInfoRepository()
        test_repository = CorpInfo(corp_info_repository)
        corp_info, status_code = test_repository.execute(request_data)

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNotNone(corp_info)

    # hostなし
    def test_get_corp_info_102_success(self):
        corp_info_repository: ICorpInfoRepository = IMockCorpInfoRepository()
        test_repository = CorpInfo(corp_info_repository)
        corp_info, status_code = test_repository.execute(None)

        self.assertEqual(status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNone(corp_info)




