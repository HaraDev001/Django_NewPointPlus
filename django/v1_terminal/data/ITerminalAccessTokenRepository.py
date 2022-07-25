from abc import ABCMeta, abstractmethod


class ITerminalAccessTokenRepository(metaclass=ABCMeta):

    @abstractmethod
    def identify(self, mail_address, password, terminal_no):
        raise NotImplementedError('identifyを実装してください')

    @abstractmethod
    def get_terminal(self, terminal_no):
        raise NotImplementedError('get_terminalを実装してください')

    @abstractmethod
    def get_terminal_access_authorization(self, mail_address, terminal_no):
        raise NotImplementedError('get_terminal_access_authorizationを実装してください')

    @abstractmethod
    def get_or_create_terminal_access_authorization(self, mail_address, terminal_no):
        raise NotImplementedError('get_or_create_terminal_access_authorizationを実装してください')

    @abstractmethod
    def save_terminal_access_authorization(self, terminal_access_auth):
        raise NotImplementedError('save_terminal_access_authorizationを実装してください')

    @abstractmethod
    def is_user_having_authority_to_user_terminal(self, mail_address, terminal) -> bool:
        raise NotImplementedError('is_user_having_authority_to_user_terminalを実装してください')
