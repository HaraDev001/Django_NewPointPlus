import uuid

from django.db import models

from .common.models import CommonModel
from .management_tag import ManagementTag


class Company(CommonModel):
    class Meta:
        db_table = 'company'
        verbose_name = verbose_name_plural = '企業情報'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    provider = models.ForeignKey(
        'database.Provider',
        verbose_name='事業者ID',
        on_delete=models.PROTECT,
    )

    company_name = models.CharField(
        verbose_name='企業名',
        max_length=255
    )

    corporate_number = models.CharField(
        verbose_name='法人番号',
        max_length=13
    )

    postal_code = models.CharField(
        verbose_name='郵便番号',
        max_length=7
    )

    address_pref = models.CharField(
        verbose_name='住所(都道府県)',
        max_length=2
    )

    address_city = models.CharField(
        verbose_name='住所(市区町村)',
        max_length=255
    )

    address_town = models.CharField(
        verbose_name='住所(町域名)',
        max_length=255,
        null=True,
    )

    address_other = models.CharField(
        verbose_name='住所(その他)',
        max_length=255,
        null=True,
    )

    phone_number = models.CharField(
        verbose_name='電話番号',
        max_length=15
    )

    management_tags = models.ManyToManyField(
        ManagementTag,
        verbose_name='管理タグ',
        null=True
    )

    available_service = models.CharField(
        verbose_name='利用可能サービス',
        max_length=255,
        default=''
    )

    available_transaction_type = models.CharField(
        verbose_name='利用可能な取引種別',
        max_length=255,
        default=''
    )

    start_available_date = models.DateField(
        verbose_name='有効開始日',
    )

    end_available_date = models.DateField(
        verbose_name='有効終了日',
        null=True
    )

    status = models.IntegerField(
        verbose_name='ステータス',
        default=0
    )

    remarks = models.CharField(
        verbose_name='備考',
        max_length=255,
        default=''
    )
