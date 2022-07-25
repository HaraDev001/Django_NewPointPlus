import uuid

from django.db import models

from .common.models import CommonModel
from .common.choices import BonusCategory


class Bonus(CommonModel):
    class Meta:
        db_table = 'bonus'
        verbose_name = verbose_name_plural = 'ボーナス情報'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    card = models.ForeignKey(
        'database.Card',
        verbose_name='カードID',
        on_delete=models.CASCADE
    )

    use_condition = models.ForeignKey(
        'database.UseCondition',
        verbose_name='利用制限ID',
        on_delete=models.SET_NULL,
        null=True
    )

    category = models.IntegerField(
        verbose_name='ボーナス種別',
        choices=BonusCategory.choices
    )

    grant_count = models.IntegerField(
        verbose_name='付与数',
        default=0
    )

    use_count = models.IntegerField(
        verbose_name='利用数',
        default=0
    )

    expired_at = models.DateField(
        verbose_name='有効期限日'
    )

    granted_at = models.DateTimeField(
        verbose_name='付与日',
        null=True
    )
