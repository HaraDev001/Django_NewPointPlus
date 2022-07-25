from datetime import datetime, timezone, timedelta
from .ICorpInfoRepository import ICorpInfoRepository
from database.models.corp_info import CorpInfo
from .exception.corp_info import CorpInfoDoesNotExist

class IDLCorpInfoRepository(ICorpInfoRepository):


    def get_corp_info(self, host):
        '''サービス情報を取得する.
            CorpInfoのmodelを返す

        Args:
            host (str型): ヘッダーのホスト.

        Returns:
            サービス情報: サービス情報を返却する.
        '''
        try:

            corp_info = CorpInfo.objects.get(host=host)
            service = {
                "e_money_card": corp_info.e_money_card
            }

            account = {
                "prepaid_value": corp_info.prepaid_value,
                "combined_bonus": corp_info.payable_bonus,
                "exchange_bonus": corp_info.exchage_bonus
            }

            corp_info_dict = {
                "host":corp_info.host,
                "company_name": corp_info.company_name,
                "service_name": corp_info.service_name,
                "logo_url": corp_info.logo_url,
                "privacy_policy_regulation_date":corp_info.privacy_policy_regulation_date,
                "privacy_policy_version": corp_info.privacy_policy_version,
                "terms_of_service_url": corp_info.terms_of_service_url,
                "terms_of_service_regulation_date": corp_info.terms_of_service_regulation_date,
                "terms_of_service_version": corp_info.terms_of_service_version,
                "privacy_policy_url": corp_info.privacy_policy_url,
                "service": service,
                "account": account,
                "copyright_notice": corpInfoData.copyright_notice
            }

            return corp_info_dict
        except CorpInfo.DoesNotExist:
            raise CorpInfoDoesNotExist()
        except Exception as e:
            raise e