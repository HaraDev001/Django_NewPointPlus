from abc import ABCMeta, abstractmethod


class ITransactionGrantRepository(metaclass=ABCMeta):

    @abstractmethod
    def grant(self, pk, card_no, terminal_no, amount, grant_method, grant_account, usage_restriction):
        raise NotImplementedError('grantを実装してください')