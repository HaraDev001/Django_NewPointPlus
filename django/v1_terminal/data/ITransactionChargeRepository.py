from abc import ABCMeta, abstractmethod


class ITransactionChargeRepository(metaclass=ABCMeta):

    @abstractmethod
    def charge(self, pk, card_no, principal_id, charge_amount, campaign_flag):
        raise NotImplementedError('chargeを実装してください')