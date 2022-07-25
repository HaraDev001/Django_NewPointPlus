from abc import ABCMeta, abstractmethod


class ITransactionUseRepository(metaclass=ABCMeta):

    @abstractmethod
    def use(self, pk, card_info_list, terminal_no):
        raise NotImplementedError('useを実装してください')