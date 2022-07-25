import uuid

from django.db import models

from .common.models import CommonModel
from .common.choices import UseConditionCategory


class UseCondition(CommonModel):

    class Meta:
        db_table = 'use_condition'
        verbose_name = verbose_name_plural = '利用制限設定情報'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    category = models.IntegerField(
        verbose_name='利用制限種別',
        choices=UseConditionCategory.choices
    )

    companies = models.ManyToManyField(
        'database.Company',
        through='UseConditionCompanyRelation',
        null=True
    )

    shops = models.ManyToManyField(
        'database.Shop',
        through='UseConditionShopRelation'
    )

    management_tags = models.ManyToManyField(
        'database.ManagementTag',
        through='UseConditionManagementTagRelation'
    )

    transaction_categories = models.ManyToManyField(
        'database.TransactionCategory',
        through='UseConditionTransactionCategoryRelation'
    )


class UseConditionCompanyRelation(CommonModel):
    class Meta:
        db_table = 'use_condition_company_relation'
        verbose_name = verbose_name_plural = '企業と利用制限の中間テーブル'

    id = models.BigAutoField(
        primary_key=True,
        editable=False
    )

    use_condition = models.ForeignKey(
        "database.UseCondition",
        on_delete=models.CASCADE,
        verbose_name='利用制限ID',
    )

    company = models.ForeignKey(
        "database.Company",
        on_delete=models.CASCADE,
        verbose_name='企業ID',
    )


class UseConditionShopRelation(CommonModel):
    class Meta:
        db_table = 'use_condition_shop_relation'
        verbose_name = verbose_name_plural = '店舗と利用制限の中間テーブル'

    id = models.BigAutoField(
        primary_key=True,
        editable=False
    )

    use_condition = models.ForeignKey(
        "database.UseCondition",
        on_delete=models.CASCADE,
        verbose_name='利用制限ID',
    )

    shop = models.ForeignKey(
        "database.Shop",
        on_delete=models.CASCADE,
        verbose_name='店舗ID',
    )


class UseConditionManagementTagRelation(CommonModel):
    class Meta:
        db_table = 'use_condition_management_tag_relation'
        verbose_name = verbose_name_plural = '管理タグと利用制限の中間テーブル'

    id = models.BigAutoField(
        primary_key=True,
        editable=False
    )

    use_condition = models.ForeignKey(
        "database.UseCondition",
        on_delete=models.CASCADE,
        verbose_name='利用制限ID',
    )

    management_tag = models.ForeignKey(
        "database.ManagementTag",
        on_delete=models.CASCADE,
        verbose_name='管理タグID',
    )


class UseConditionTransactionCategoryRelation(CommonModel):
    class Meta:
        db_table = 'use_condition_transaction_category_relation'
        verbose_name = verbose_name_plural = '取引種別と利用制限の中間テーブル'

    id = models.BigAutoField(
        primary_key=True,
        editable=False
    )

    use_condition = models.ForeignKey(
        "database.UseCondition",
        on_delete=models.CASCADE,
        verbose_name='利用制限ID',
    )

    transaction_category = models.ForeignKey(
        "database.TransactionCategory",
        on_delete=models.CASCADE,
        verbose_name='取引種別ID',
    )
