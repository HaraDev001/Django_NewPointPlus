from abc import ABCMeta, abstractmethod


class ICardActivateRepository(metaclass=ABCMeta):

    @abstractmethod
    def identify_card(self, card_no, card_pin):
        raise NotImplementedError('identify_cardを実装してください')

    @abstractmethod
    def get_terminal_authorization_by_access_token(
            self, terminal_access_token):
        raise NotImplementedError(
            'get_terminal_authorization_by_access_tokenを実装してください')

    @abstractmethod
    def save_card(self, card_no):
        raise NotImplementedError('activate_cardを実装してください')
