from abc import ABCMeta, abstractmethod


class ITransactionCancelRepository(metaclass=ABCMeta):

    @abstractmethod
    def get_transaction(self, transaction_id):
        raise NotImplementedError('get_transactionを実装してください')

    @abstractmethod
    def get_or_create_transaction(self, transaction_id):
        raise NotImplementedError('get_or_create_transactionを実装してください')

    @abstractmethod
    def get_card_transactions_by_transaction_id(self, transaction_id):
        raise NotImplementedError('get_card_transactions_by_transaction_idを実装してください')

    @abstractmethod
    def get_balances_from_card_transaction_list(self, card_transaction_list):
        raise NotImplementedError('get_balances_from_card_transaction_listを実装してください')

    @abstractmethod
    def get_balances_by_card_no(self, card_no):
        raise NotImplementedError('get_balances_by_card_noを実装してください')

    @abstractmethod
    def create_cancel_card_transaction(
                                    self,
                                    terminal,
                                    cancel_transaction,
                                    new_transaction_id,
                                    new_transaction_type,
                                    new_transaction_at):
        raise NotImplementedError('create_cancel_card_transactionを実装してください')

    @abstractmethod
    def create_cancel_transaction(self, terminal, new_transaction_id, cancel_target_transaction_id):
        raise NotImplementedError('create_cancel_transactionを実装してください')

    @abstractmethod
    def cancel_transaction(self, terminal, transaction_id, cancel_target_transaction_id):
        raise NotImplementedError('cancel_transactionを実装してください')

    @abstractmethod
    def save_new_transaction(self, cancel_target_transacion, new_transaction, new_card_transaction_list):
        raise NotImplementedError('save_new_transactionを実装してください')

    @abstractmethod
    def make_response(self,
                      canceled_transaction_type,
                      cancel_at,
                      terminal,
                      balance,
                      balance_before_cancel,
                      balance_after_cancel,
                      new_card_transaction_list,
                      ):
        raise NotImplementedError('make_responseを実装してください')
