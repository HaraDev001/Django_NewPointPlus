
class TransactionCancelCompany:
    def __init__(self, company_id, company_name):
        self.company_id = company_id
        self.company_name = company_name


class TransactionCancelShop:
    def __init__(self, shop_id, shop_name):
        self.shop_id = shop_id
        self.shop_name = shop_name


class TransactionCancelTransaction:
    def __init__(self, transaction_amount, value_amount,
                 payable_bonus_amount, product_exchange_amount):
        self.transaction_amount = transaction_amount
        self.value_amount = value_amount
        self.payable_bonus_amount = payable_bonus_amount
        self.product_exchange_amount = product_exchange_amount


class TransactionCancelBalance:
    def __init__(self, value_balance, value_expire_at,
                 payable_bonus_balance, product_exchange_bonus_balance):
        self.value_balance = value_balance
        self.value_expire_at = value_expire_at
        self.payable_bonus_balance = payable_bonus_balance
        self.product_exchange_bonus_balance = product_exchange_bonus_balance


class TransactionCancelCampaign:
    def __init__(self, event_name, cancel_grant_bank_account,
                 cancel_grant_count, expire_at):
        self.event_name = event_name
        self.cancel_grant_bank_account = cancel_grant_bank_account
        self.cancel_grant_count = cancel_grant_count
        self.expire_at = expire_at


class TransactionCancelCard:
    def __init__(self, card_config_name, card_no,
                 balance_before_cancel, balance_after_cancel, campaign):
        self.card_config_name = card_config_name
        self.card_no = card_no
        # 取引前残高
        self.balance_before_cancel = balance_before_cancel
        # 取引後残高
        self.balance_after_cancel = balance_after_cancel

        # キャンペーン
        self.campaign = campaign


class TransactionCancelResponse:
    '''TransactionCancelResponseクラス

        取引取消を実行するCancelTransactionからSerializerへ渡されるDTOクラス

        Attributes:
            transaction_type (int型): 新しい取引種別.
            transaction_at (datetime型): 新しい取引の取引日時.
    '''

    def __init__(
        self, transaction_type, transaction_at,
        company, shop, terminal_no, transaction_cancel, card
    ):
        self.transaction_type = transaction_type
        self.transaction_at = transaction_at

        self.company = company
        self.shop = shop
        self.terminal_no = terminal_no
        self.transaction_cancel = transaction_cancel
        self.card = card
