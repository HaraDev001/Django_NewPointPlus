from v1_card.data.ICorpInfoRepository import ICorpInfoRepository
from rest_framework import status


class CorpInfo:
    '''
        CorpInfoクラス
        Attributes:
            corp_info_repository(ICorpInfoRepository型):
            ICorpInfoRepositoryを継承したオブジェクト
    '''

    def __init__(self, corp_info_repository: ICorpInfoRepository):
        self.corp_info_repository: ICorpInfoRepository = corp_info_repository

    def execute(self, host):
        '''サービス情報取得APIを取得する.
            サービス情報取得APIを取得する.

        Returns:
            サービス情報取得API: サービス情報取得APIを返却する.
        '''
        try:
            corp_info = self.corp_info_repository.get_corp_info(host)
        except Exception:
            return None, status.HTTP_400_BAD_REQUEST

        return corp_info, status.HTTP_200_OK