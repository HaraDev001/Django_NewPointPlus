from abc import ABCMeta, abstractmethod


class ICardDetailRepository(metaclass=ABCMeta):
    @abstractmethod
    def identify_card(self, card_no, card_pin):
        raise NotImplementedError('identify_cardを実装してください')

    @abstractmethod
    def get_terminal_authorization_by_access_token(
            self, card_no, terminal_access_token):
        raise NotImplementedError(
            'get_terminal_authorization_by_access_tokenを実装してください')

    @abstractmethod
    def get_card_config_by_no(self, card_no):
        raise NotImplementedError('get_card_config_by_noを実装してください')

    @abstractmethod
    def get_card_transaction_by_no(self, card_no):
        raise NotImplementedError('get_card_transaction_by_noを実装してください')
