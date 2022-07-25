from datetime import datetime, timezone, timedelta
from .ICorpInfoRepository import ICorpInfoRepository
from unittest import mock


class IMockCorpInfoRepository(ICorpInfoRepository):
    '''
    ICorpInfoRepositoryを実装したクラス
        ICorpInfoRepositoryを実装したモックオブジェクトを扱うクラス
        Attributes:
            corp_info_list (dict): サービス情報を保持
    '''
    def __init__(self):
        self.corp_info_list = dict()

        JST = timezone(timedelta(hours=+9), 'JST')

        service_1 = mock.MagicMock(e_money_card=1)
        service_2 = mock.MagicMock(e_money_card=0)

        account_1 = mock.MagicMock(prepaid_value=1, combined_bonus=1, exchange_bonus=1)
        account_2 = mock.MagicMock(prepaid_value=0, combined_bonus=1, exchange_bonus=1)

        corp_info1 = mock.MagicMock(
                                    host='localhost:8000',
                                    company_name='テスト事業者',
                                    service_name='テストサービス',
                                    logo_url='https://company/logo.png',
                                    privacy_policy_regulation_date=datetime(2021 , 7 , 3 , 12 , 30, tzinfo=JST),
                                    privacy_policy_version='1.0.0',
                                    terms_of_service_url='https://company/terms.html',
                                    terms_of_service_regulation_date=datetime(2021 , 7 , 3 , 12 , 30, tzinfo=JST),
                                    terms_of_service_version='1.0.0',
                                    privacy_policy_url='https://company/policy.html',
                                    service=service_1,
                                    account=account_1,
                                    copyright_notice='Copyright notice'
                                    )

        corp_info2 = mock.MagicMock(
                                    host='host:8001',
                                    company_name='テスト事業者',
                                    service_name='テストサービス',
                                    logo_url='https://company/logo.png',
                                    privacy_policy_regulation_date=datetime(2021 , 7 , 3 , 12 , 30, tzinfo=JST),
                                    privacy_policy_version='1.0.0',
                                    terms_of_service_url='https://company/terms.html',
                                    terms_of_service_regulation_date=datetime(2021 , 7 , 3 , 12 , 30, tzinfo=JST),
                                    terms_of_service_version='1.0.0',
                                    privacy_policy_url='https://company/policy.html',
                                    service=service_2,
                                    account=account_2,
                                    copyright_notice='Copyright notice'
                                    )

        for corp_info in [corp_info1, corp_info2]:
            key = corp_info.host
            self.corp_info_list[key] = corp_info

    def get_corp_info(self, host):
        '''サービス情報を取得する.
            サービス情報を取得する.

        Args:
            host (str型): ヘッダーのホスト.

        Returns:
            サービス情報: サービス情報を返却する.
        '''
        try:
            return self.corp_info_list[host]
        except KeyError:
            raise Exception('リクエストされたホストで一致するサービス情報がない')
        except Exception as e:
            raise e