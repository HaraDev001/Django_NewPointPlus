import uuid

from django.db import models

from .common.models import CommonModel
from .common.choices import ValueCategory


class Value(CommonModel):
    class Meta:
        db_table = 'value'
        verbose_name = verbose_name_plural = 'バリュー情報'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    card = models.ForeignKey(
        'database.Card',
        verbose_name='カードID',
        on_delete=models.PROTECT
    )

    use_condition = models.ForeignKey(
        'database.UseCondition',
        verbose_name='利用制限ID',
        on_delete=models.SET_NULL,
        null=True
    )

    campaign = models.ForeignKey(
        'database.Campaign',
        verbose_name='付与キャンペーンID',
        on_delete=models.SET_NULL,
        null=True
    )

    category = models.IntegerField(
        verbose_name='バリュー種別',
        choices=ValueCategory.choices,
        default=ValueCategory.PREPAID
    )

    amount = models.IntegerField(
        verbose_name='残高',
        default=0
    )

    expired_at = models.DateTimeField(
        verbose_name='有効期限日'
    )

    is_charge_value = models.BooleanField(
        verbose_name='チャージバリューフラグ',
        default=True
    )

    granted_at = models.DateTimeField(
        verbose_name='付与日',
        null=True
    )
