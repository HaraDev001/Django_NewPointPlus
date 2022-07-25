from abc import ABCMeta, abstractmethod


class IIssueTransactionNumberRepository(metaclass=ABCMeta):

    @abstractmethod
    def issue_transaction_number(self):
        raise NotImplementedError(
            'issue_transaction_numberを実装してください')

    @abstractmethod
    def get_terminal_authorization_by_access_token(
            self, terminal_access_token):
        raise NotImplementedError(
            'get_terminal_authorization_by_access_tokenを実装してください')

    @abstractmethod
    def create_transaction(self, transaction_number):
        raise NotImplementedError(
            'create_transactionを実装してください')
