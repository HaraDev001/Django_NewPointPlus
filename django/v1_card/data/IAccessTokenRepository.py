from abc import ABCMeta, abstractmethod


class IAccessTokenRepository(metaclass=ABCMeta):

    @abstractmethod
    def identify_card(self, card_no, card_pin):
        raise NotImplementedError('identify_cardを実装してください')

    @abstractmethod
    def get_card(self, card_no):
        raise NotImplementedError('get_cardを実装してください')

    @abstractmethod
    def get_card_access_authorization(self, card_no):
        raise NotImplementedError('get_card_access_authorizationを実装してください')

    @abstractmethod
    def get_or_create_card_access_authorization(self, card_no):
        raise NotImplementedError('get_or_create_card_access_authorizationを実装してください')

    @abstractmethod
    def save_card_access_authorization(self, card_access_auth):
        raise NotImplementedError('save_card_access_authorizationを実装してください')
