import uuid
from datetime import datetime, timedelta, timezone

from django.db import models

from .common.choices import (BonusCategory, BonusExtendExpirationUnit,
                             CampaignEnableTimingCategory, DayOfWeek,
                             TaxPercentRoundType, TransactionCategory)
from .common.models import CommonModel

JST = timezone(timedelta(hours=+9))


class Campaign(CommonModel):

    class Meta:
        db_table = 'campaign'
        verbose_name = verbose_name_plural = 'キャンペーン情報'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    card_config = models.ManyToManyField(
        'database.CardConfig',
        through="CampaignCardConfigRelation"
    )

    campaign_name = models.CharField(
        verbose_name='キャンペーン名',
        max_length=191,
        default=''
    )

    start_campaign_at = models.DateTimeField(
        verbose_name='キャンペーン開始日時',
        default=datetime.now(JST)
    )

    end_campaign_at = models.DateTimeField(
        verbose_name='キャンペーン終了日時',
        default=datetime.max
    )

    priority = models.IntegerField(
        verbose_name='キャンペーン適用優先順位',
        default=1
    )

    is_limit_over_grant_allowed = models.BooleanField(
        verbose_name='ボーナス付与上限超過可否',
        default=False
    )

    tax_percent = models.IntegerField(
        verbose_name='消費税',
        default=0
    )

    tax_percent_round_type = models.IntegerField(
        verbose_name='消費税小数値',
        choices=TaxPercentRoundType.choices,
        default=TaxPercentRoundType.ROUND_DOWN
    )

    note = models.CharField(
        verbose_name='備考',
        max_length=191,
        default=''
    )


class CampaignCardConfigRelation(models.Model):

    class Meta:
        db_table = 'campaign_card_config_relation'
        verbose_name = verbose_name_plural = 'キャンペーンとカード設定の中間テーブル'

    id = models.BigAutoField(
        primary_key=True,
        editable=False
    )

    campaign = models.ForeignKey(
        'database.Campaign',
        verbose_name='キャンペーンID',
        on_delete=models.CASCADE
    )

    card_config = models.ForeignKey(
        'database.CardConfig',
        verbose_name='カード設定ID',
        on_delete=models.CASCADE
    )


class CampaignBonusConfig(CommonModel):

    class Meta:
        db_table = 'campaign_bonus_config'
        verbose_name = verbose_name_plural = 'キャンペーン付与ボーナス設定情報'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    campaign = models.ForeignKey(
        'database.Campaign',
        verbose_name='キャンペーンID',
        on_delete=models.CASCADE,
        null=True
    )

    use_condition = models.ForeignKey(
        'database.UseCondition',
        verbose_name='利用制限ID',
        on_delete=models.SET_NULL,
        null=True
    )

    category = models.IntegerField(
        verbose_name='ボーナス種別',
        choices=BonusCategory.choices,
        default=BonusCategory.PAYABLE
    )

    bonus_expiration_unit = models.IntegerField(
        verbose_name='有効期限カウント単位',
        choices=BonusExtendExpirationUnit.choices,
        null=True
    )

    bonus_expiration_count = models.IntegerField(
        verbose_name='有効期限カウント数',
        null=True
    )

    bonus_expiration_date = models.DateField(
        verbose_name='有効期限指定日',
        null=True
    )


class CampaignApplyRuleActiveTiming(CommonModel):

    class Meta:
        db_table = 'campaign_apply_rule_active_timing'
        verbose_name = verbose_name_plural = 'キャンペーン適用対象タイミング情報'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    campaign = models.ForeignKey(
        'database.Campaign',
        verbose_name='キャンペーンID',
        on_delete=models.CASCADE
    )

    active_timing_category = models.IntegerField(
        verbose_name='有効タイミング種別',
        choices=CampaignEnableTimingCategory.choices,
        default=CampaignEnableTimingCategory.ALWAYS
    )

    active_start_at = models.TimeField(
        verbose_name='キャンペーン有効開始時間',
        null=True
    )

    active_end_at = models.TimeField(
        verbose_name='キャンペーン有効終了時間',
        null=True
    )

    active_day_of_week = models.IntegerField(
        verbose_name='キャンペーン有効曜日',
        choices=DayOfWeek.choices,
        null=True
    )

    active_target_day = models.IntegerField(
        verbose_name='キャンペーン有効指定日',
        null=True
    )

    active_target_month = models.IntegerField(
        verbose_name='キャンペーン有効指定月',
        null=True
    )

    active_start_date = models.DateField(
        verbose_name='キャンペーン有効指定開始日',
        null=True
    )

    active_end_date = models.DateField(
        verbose_name='キャンペーン有効指定終了日',
        null=True
    )


class CampaignApplyRulePlace(CommonModel):

    class Meta:
        db_table = 'campaign_apply_rule_place'
        verbose_name = verbose_name_plural = 'キャンペーン適用対象取引場所情報'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    campaign = models.ForeignKey(
        'database.Campaign',
        verbose_name='キャンペーンID',
        on_delete=models.CASCADE
    )

    target_company = models.ForeignKey(
        'database.Company',
        verbose_name='対象企業',
        on_delete=models.CASCADE,
        null=True
    )

    target_shop = models.ForeignKey(
        'database.Shop',
        verbose_name='対象店舗',
        on_delete=models.CASCADE,
        null=True
    )

    target_management_tag = models.ForeignKey(
        'database.ManagementTag',
        verbose_name='対象管理タグ',
        on_delete=models.CASCADE,
        null=True
    )

    target_prefectures = models.ForeignKey(
        'database.Prefectures',
        verbose_name='対象都道府県',
        on_delete=models.CASCADE,
        null=True
    )

    target_city = models.CharField(
        verbose_name='対象市区町村',
        max_length=191,
        null=True
    )


class CampaignApplyRuleTransactionCategory(CommonModel):
    class Meta:
        db_table = 'campaign_apply_rule_transaction_category'
        verbose_name = verbose_name_plural = 'キャンペーン適用対象取引種別情報'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    campaign = models.ForeignKey(
        Campaign,
        verbose_name='キャンペーンID',
        on_delete=models.CASCADE
    )

    transaction_category = models.IntegerField(
        verbose_name='対象取引種別',
        choices=TransactionCategory.choices
    )


class CampaignApplyRuleTransactionDetail(CommonModel):

    class Meta:
        db_table = 'campaign_apply_rule_transaction_detail'
        verbose_name = verbose_name_plural = 'キャンペーン適用対象取引詳細情報'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    campaign = models.ForeignKey(
        Campaign,
        verbose_name='キャンペーンID',
        on_delete=models.CASCADE
    )

    grant_count = models.IntegerField(
        verbose_name='付与数/率',
        default=0
    )

    min_amount = models.IntegerField(
        verbose_name='対象最低取引金額',
        null=True
    )

    max_amount = models.IntegerField(
        verbose_name='対象最高取引金額',
        null=True
    )

    count_category = models.IntegerField(
        verbose_name='取引回数種別',
        null=True
    )

    min_count = models.IntegerField(
        verbose_name='対象最低取引回数',
        null=True
    )

    max_count = models.IntegerField(
        verbose_name='対象最高取引回数',
        null=True
    )

    days_category = models.IntegerField(
        verbose_name='取引日数種別',
        null=True
    )

    min_days = models.IntegerField(
        verbose_name='対象最低取引日数',
        null=True
    )

    max_days = models.IntegerField(
        verbose_name='対象最高取引日数',
        null=True
    )


class CampaignApplyRuleCardActivateDate(CommonModel):

    class Meta:
        db_table = 'campaign_apply_rule_card_activate_date'
        verbose_name = verbose_name_plural = 'キャンペーン適用対象アクティベート日情報'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    campaign = models.ForeignKey(
        Campaign,
        verbose_name='キャンペーンID',
        on_delete=models.CASCADE
    )

    start_target_at = models.DateTimeField(
        verbose_name='対象開始日',
        null=True
    )

    end_target_at = models.DateTimeField(
        verbose_name='対象終了日',
        null=True
    )
