from abc import ABCMeta, abstractmethod


class ITransactionGetRepository(metaclass=ABCMeta):
    @abstractmethod
    def get_card(self, card_no):
        raise NotImplementedError('get_cardを実装してください')

    @abstractmethod
    def get_terminal_authorization(self, card_number, search):
        raise NotImplementedError('get_terminal_authorizationを実装してください')

    @abstractmethod
    def get_transaction_list(
        self, transaction_type, transaction_start, transaction_end, transaction_status,
        terminal_no, card_no, magnetic_information
    ):
        raise NotImplementedError('get_transaction_listを実装してください')

    @abstractmethod
    def get_transaction(self, transaction_number):
        raise NotImplementedError('get_transactionを実装してください')
