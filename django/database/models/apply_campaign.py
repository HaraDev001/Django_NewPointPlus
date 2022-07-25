import uuid

from django.db import models

from .common.models import CommonModel
from .common.choices import BonusCategory


class ApplyCampaign(CommonModel):

    class Meta:
        db_table = 'apply_campaign'
        verbose_name = verbose_name_plural = 'キャンペーン適用履歴情報'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    campaign = models.ForeignKey(
        'database.Campaign',
        verbose_name='適用キャンペーンID',
        on_delete=models.SET_NULL,
        max_length=32,
        null=True
    )

    campaign_name = models.CharField(
        verbose_name='適用キャンペーン名',
        max_length=191
    )

    card_transaction = models.ForeignKey(
        'database.CardTransaction',
        verbose_name='適用対象カード取引履歴ID',
        on_delete=models.PROTECT,
        max_length=32
    )

    applied_at = models.DateTimeField(
        verbose_name='適用日時'
    )

    bonus = models.ForeignKey(
        'database.Bonus',
        verbose_name='付与ボーナスID',
        on_delete=models.PROTECT,
        max_length=32
    )

    bonus_category = models.IntegerField(
        verbose_name='付与ボーナス種別',
        choices=BonusCategory.choices,
        default=BonusCategory.PAYABLE
    )

    bonus_grant_count = models.IntegerField(
        verbose_name='付与ボーナス数',
        default=0
    )

    bonus_expired_at = models.DateField(
        verbose_name='付与ボーナス有効期限日'
    )
