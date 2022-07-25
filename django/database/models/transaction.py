import uuid

from django.db import models
from django.utils import timezone

from .common.models import CommonModel
from .common.choices import TransactionCategory, CampaignApplyTiming, TransactionMethod, TransactionStatus, ChargePaymentMethod


# Luan note: API lien quan:
class Transaction(CommonModel):
    class Meta:
        db_table = 'transaction'
        ordering = ['transaction_at']
        verbose_name = verbose_name_plural = '取引履歴情報'

    transaction_number = models.BigAutoField(
        primary_key=True,
        editable=False
    )

    id = models.UUIDField(
        default=uuid.uuid4,
        editable=False
    )

    transaction_at = models.DateTimeField(
        help_text="ミリ秒の差異発生を考慮して登録日/更新日とは別に持つ",
        verbose_name='取引日時',
        default=timezone.now
    )

    category = models.SmallIntegerField(
        verbose_name='取引種別',
        choices=TransactionCategory.choices
    )

    status = models.SmallIntegerField(
        verbose_name='取引状態',
        choices=TransactionStatus.choices,
        default=TransactionStatus.INCOMPLETE
    )

    provider = models.ForeignKey(
        "database.Provider",
        on_delete=models.CASCADE,
        verbose_name='事業者ID',
    )

    company = models.ForeignKey(
        'database.Company',
        verbose_name='企業ID',
        on_delete=models.SET_NULL,
        null=True
    )

    shop = models.ForeignKey(
        'database.Shop',
        verbose_name='店舗ID',
        on_delete=models.SET_NULL,
        null=True
    )

    terminal = models.ForeignKey(
        'database.Terminal',
        verbose_name='店舗端末ID',
        on_delete=models.SET_NULL,
        null=True
    )

    consumer = models.ForeignKey(
        "database.Consumer",
        verbose_name='消費者アカウントID',
        on_delete=models.SET_NULL,
        null=True
    )

    total_prepaid_value_amount = models.IntegerField(
        default=0,
        verbose_name="前払いバリュー取引総額"
    )

    total_payable_bonus_amount = models.IntegerField(
        default=0,
        verbose_name="決済併用ボーナス取引総数"
    )

    total_exchange_bonus_amount = models.IntegerField(
        default=0,
        verbose_name="商品交換ボーナス取引総数"
    )

    campaign_apply_timing = models.SmallIntegerField(
        verbose_name='キャンペーン適用タイミング',
        help_text="""
            NOT_APPLY = 0
            SYNC = 1
            ASYNC = 2
        """,
        choices=CampaignApplyTiming.choices,
        default=CampaignApplyTiming.NOT_APPLY
    )

    parent_transaction = models.ForeignKey(
        "self",
        null=True,
        on_delete=models.PROTECT
    )

    operator = models.CharField(
        max_length=191,
        null=True
    )

    transaction_method = models.SmallIntegerField(
        verbose_name='取引方式',
        help_text="""
            TERMINAL = 1
            CPM = 2
            MPM = 3
        """,
        choices=TransactionMethod.choices,
        default=TransactionMethod.TERMINAL
    )

    charge_payment_method = models.IntegerField(
        verbose_name='チャージ金支払い方法',
        choices=ChargePaymentMethod.choices,
        null=True
    )
