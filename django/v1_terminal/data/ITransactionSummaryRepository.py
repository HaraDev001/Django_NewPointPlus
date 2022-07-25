from abc import ABCMeta, abstractmethod


class ITransactionSummaryRepository(metaclass=ABCMeta):

    @abstractmethod
    def summary(self, search):
        raise NotImplementedError('summaryを実装してください')