from abc import ABCMeta, abstractmethod


class ITransactionPayRepository(metaclass=ABCMeta):

    @abstractmethod
    def pay(self, pk, card_info_list, terminal_no, charge_amount, campaign_flag):
        raise NotImplementedError('payを実装してください')