from abc import ABCMeta, abstractmethod


class ICardDetailRepository(metaclass=ABCMeta):
    @abstractmethod
    def get_card_by_no(self, card_no):
        raise NotImplementedError('get_cardを実装してください')

    @abstractmethod
    def get_card_config_by_no(self, card_no):
        raise NotImplementedError('get_card_config_by_noを実装してください')

    @abstractmethod
    def get_card_transaction_by_no(self, card_no):
        raise NotImplementedError('get_card_transaction_by_noを実装してください')

    @abstractmethod
    def get_card_access_authorization_by_no(self, card_no, card_access_auth):
        raise NotImplementedError(
            'get_card_access_authorization_by_noを実装してください')
