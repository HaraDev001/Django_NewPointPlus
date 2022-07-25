from abc import ABCMeta, abstractmethod


class ICorpInfoRepository(metaclass=ABCMeta):
    @abstractmethod
    def get_corp_info(self):
        raise NotImplementedError('get_corp_infoを実装してください')