from django.db import models
from django.utils.translation import gettext_lazy as _


class DayOfWeek(models.IntegerChoices):
    MON = 0, _('mon')
    TUE = 1, _('tue')
    WED = 2, _('wed')
    THU = 3, _('thu')
    FRI = 4, _('fri')
    SAT = 5, _('sat')
    SUN = 6, _('sun')


class CardStatus(models.IntegerChoices):
    NOT_ACTIVATED = 1, _('not_activated')
    ACTIVATED = 2, _('activated')
    STOPPED = 3, _('stopped')
    MERGED = 4, _('merged')
    DESTROYED = 5, _('destroyed')


class CardCategory(models.IntegerChoices):
    E_MONEY = 1, _('e_money')
    GIFT = 2, _('gift')


class TransactionCategory(models.IntegerChoices):
    PAYMENT = 1, _('payment')
    PAYMENT_CANCEL = -1, _('payment_cancel')
    CHARGE = 2, _('charge')
    CHARGE_CANCEL = -2, _('charge_cancel')
    GRANT = 3, _('grant')
    GRANT_CANCEL = -3, _('grant_cancel')
    USE_BONUS = 4, _('use_bonus')
    USE_BONUS_CANCEL = -4, _('use_bonus_cancel')
    EXPIRED = 5, _('expired')
    CARD_ACTIVATE = 6, _('card_activate')
    CARD_LOCK = 7, _('card_lock')
    CARD_UNLOCK = -7, _('card_unlock')
    CARD_MERGE = 8, _('card_merge')
    CARD_STOP = 9, _('card_stop')
    CARD_UNSTOP = -9, _('card_unstop')
    CARD_DESTROY = 10, _('card_destroy')


class TransactionStatus(models.IntegerChoices):
    INCOMPLETE = 1, _('incomplete')
    COMPLETED = 2, _('completed')


class TransactionChargeFrom(models.IntegerChoices):
    CASH = 1, _('cash')
    CREDIT_CARD = 2, _('credit_card')
    BANK = 3, _('bank')


class TransactionMethod(models.IntegerChoices):
    TERMINAL = 1, _('terminal'),
    CPM = 2, _('cpm'),
    MPM = 3, _('mpm')


class ChargePaymentMethod(models.IntegerChoices):
    CASH = 1, _('cash'),
    CREDIT_CARD = 2, _('credit_card'),


class ValueCategory(models.IntegerChoices):
    PREPAID = 1, _('prepaid')
    FUND_TRANSFER = 2, _('fund_transfer')
    SPECIALLY = 3, _('specially')


class BonusCategory(models.IntegerChoices):
    PAYABLE = 1, _('payable')
    EXCHANGE = 2, _('exchange')


class BonusExtendExpirationUnit(models.IntegerChoices):
    NOTHING = 0, _('nothing')
    DAY = 1, _('day')
    WEEK = 2, _('week')
    MONTH = 3, _('month')
    YEAR = 4, _('year')


class UseConditionCategory(models.IntegerChoices):
    COMPANY = 1, _('company')
    SHOP = 2,  _('shop')
    MANAGEMENT_TAG = 3, _('management_tag')
    TRANSACTION_CATEGORY = 4, _('transaction_category')


class TaxPercentRoundType(models.IntegerChoices):
    ROUND_DOWN = 0, _('round_down')
    ROUND_UP = 1, _('round_up')
    ROUND_OFF = 2, _('round_off')


class CampaignApplyTiming(models.IntegerChoices):
    NOT_APPLY = 0, _('not_apply')
    SYNC = 1, _('sync')
    ASYNC = 2, _('async')


class CampaignEnableTimingCategory(models.IntegerChoices):
    ALWAYS = 0, _('always')
    SELECT_TIME = 1, _('select_time')
    SELECT_DAY_OF_WEEK = 2, _('select_day_of_week')
    SELECT_DAY = 3, _('select_day'),
    SELECT_DAY_AND_MONTH = 4, _('select_day_and_month'),
    SELECT_PERIOD = 5, _('select_period'),


class ProviderStatus(models.IntegerChoices):
    ACTIVE = 1, _('active')
    NOT_AGREE = 2, _('not_agree')
    DISABLED = 3, _('disabled')
    REVIEWING = 4, _('reviewing')
    DELETED = 5, _('deleted')


class TerminalCategory(models.IntegerChoices):
    POS = 1, _('pos')
    PAYMENT_TERMINAL = 2, _('payment_terminal')
    CHARGE_TERMINAL = 3, _('charge_terminal')


class ManagementTagCategory(models.IntegerChoices):
    COMPANY = 1, _('prepaid')
    SHOP = 2, _('shop')
    TERMINAL = 3, _('terminal')
    CONSUMER = 4, _('consumer')
