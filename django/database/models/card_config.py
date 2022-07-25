import uuid

from django.db import models

from .common.models import CommonModel
from .common.choices import CardCategory


class CardConfig(CommonModel):

    class Meta:
        db_table = 'card_config'
        verbose_name = verbose_name_plural = 'カード設定情報'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    provider = models.ForeignKey(
        'database.Provider',
        verbose_name='事業者ID',
        on_delete=models.CASCADE
    )

    card_name = models.CharField(
        verbose_name='カード名称',
        max_length=191
    )

    card_category = models.IntegerField(
        verbose_name='カード種別',
        choices=CardCategory.choices,
        default=CardCategory.E_MONEY
    )

    exists_physics_card = models.BooleanField(
        verbose_name='物理カード存在フラグ',
        default=True
    )

    is_promotion_card = models.BooleanField(
        verbose_name='販促カードフラグ',
        default=False
    )

    card_design_url = models.URLField(
        verbose_name='カードデザインURL',
        max_length=2048
    )

    prepaid_value_name = models.CharField(
        verbose_name='前払いバリュー名称',
        max_length=191
    )

    prepaid_value_currency_unit = models.CharField(
        verbose_name='前払いバリュー通貨単位',
        max_length=191
    )

    prepaid_value_balance_limit = models.IntegerField(
        verbose_name='前払いバリュー残高上限値'
    )

    payable_bonus_name = models.CharField(
        verbose_name='決済併用ボーナス名称',
        max_length=191,
        default=''
    )

    payable_bonus_currency_unit = models.CharField(
        verbose_name='決済併用ボーナス通貨単位',
        max_length=191
    )

    payable_bonus_balance_limit = models.IntegerField(
        verbose_name='決済併用ボーナス残高上限値'
    )

    exchange_bonus_name = models.CharField(
        verbose_name='決済併用ボーナス名称',
        max_length=191
    )

    exchange_bonus_currency_unit = models.CharField(
        verbose_name='決済併用ボーナス通貨単位',
        max_length=191
    )

    exchange_bonus_balance_limit = models.IntegerField(
        verbose_name='決済併用ボーナス残高上限値'
    )

    start_apply_at = models.DateTimeField(
        verbose_name='適用開始日時'
    )

    end_apply_at = models.DateTimeField(
        verbose_name='適用終了日時',
        null=True
    )
