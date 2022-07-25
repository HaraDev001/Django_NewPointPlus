import uuid

from django.db import models

from .common.models import CommonModel


class CardConfigPayment(CommonModel):
    class Meta:
        db_table = 'card_config_payment'
        verbose_name = verbose_name_plural = 'カード決済設定情報'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    card_config = models.ForeignKey(
        'database.CardConfig',
        verbose_name='カード設定ID',
        on_delete=models.CASCADE
    )

    payment_limit_daily = models.IntegerField(
        verbose_name='チャージ可能額(日)',
        default=500000
    )

    payment_limit_monthly = models.IntegerField(
        verbose_name='チャージ可能額(月)',
        default=2000000
    )

    start_apply_at = models.DateTimeField(
        verbose_name='適用開始日時'
    )

    end_apply_at = models.DateTimeField(
        verbose_name='適用終了日時',
        null=True
    )
