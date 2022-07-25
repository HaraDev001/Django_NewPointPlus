from abc import ABCMeta, abstractmethod


class ICardBalanceRepository(metaclass=ABCMeta):
    @abstractmethod
    def get_card_balance_by_type(self, card_no, balance_type):
        raise NotImplementedError('get_card_balance_by_typeを実装してください')
