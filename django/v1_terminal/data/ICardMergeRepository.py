from abc import ABCMeta, abstractmethod


class ICardMergeRepository(metaclass=ABCMeta):

    @abstractmethod
    def get_card_balances(self, card_id, balance_type):
        raise Exception('get_card_balancesを実装してください')

    @abstractmethod
    def get_value_config(self, value_config_id):
        raise Exception('get_value_configを実装してください')

    @abstractmethod
    def get_bonus_config(self, bonus_config_id):
        raise Exception('get_bonus_configを実装してください')

    @abstractmethod
    def enumerate_balance_list(self, balance_list, balance_type, value_or_bonus_type):
        raise Exception('enumerate_balance_listを実装してください')

    @abstractmethod
    def merge_value(self, merge_from, merge_to):
        raise Exception('merge_valueを実装してください')

    @abstractmethod
    def merge_bonus(self, merge_from, merge_to):
        raise Exception('merge_bonusを実装してください')

    @abstractmethod
    def verify_over_limit(self, merge_from, merge_to):
        raise Exception('verify_over_limitを実装してください')

    @abstractmethod
    def get_summary(self, key_name, merge_from, merge_to):
        raise Exception('get_summaryを実装してください')

    @abstractmethod
    def merge(self, merge_from, merge_to):
        raise Exception('mergeを実装してください')

    @abstractmethod
    def make_response(self):
        raise Exception('make_responseを実装してください')
