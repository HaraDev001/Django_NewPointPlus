from abc import ABCMeta, abstractmethod


class ITransactionRepository(metaclass=ABCMeta):
    @abstractmethod
    def get_transaction(self, card_no, transaction_id):
        raise NotImplementedError('get_transactionを実装してください')

    @abstractmethod
    def get_transaction_list(self, card_number, search):
        raise NotImplementedError('get_transaction_listを実装してください')