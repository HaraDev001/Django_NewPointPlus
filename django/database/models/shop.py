import uuid

from django.db import models

from .common.models import CommonModel
from .management_tag import ManagementTag
from .business_type import BusinessType


class Shop(CommonModel):

    class Meta:
        db_table = 'shop'
        verbose_name = verbose_name_plural = '店舗情報'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    company = models.ForeignKey(
        'database.Company',
        verbose_name='企業ID',
        on_delete=models.CASCADE
    )

    provider = models.ForeignKey(
        'database.Provider',
        verbose_name='企業ID',
        on_delete=models.CASCADE
    )

    business_type = models.ForeignKey(
        BusinessType,
        verbose_name='業種ID',
        on_delete=models.PROTECT
    )

    shop_name = models.CharField(
        verbose_name='店舗名',
        max_length=191,
        default=''
    )

    shop_name_english_characters = models.CharField(
        verbose_name='店舗名ローマ字',
        max_length=191,
        default=''
    )

    shop_number = models.CharField(
        verbose_name='店舗番号',
        max_length=191,
        default=''
    )

    postal_code = models.CharField(
        verbose_name='郵便番号',
        max_length=191,
        default=''
    )

    address_pref = models.ForeignKey(
        'database.Prefectures',
        verbose_name='都道府県ID',
        on_delete=models.PROTECT
    )

    address_city = models.CharField(
        verbose_name='住所(市区町村)',
        max_length=191,
        default=''
    )

    address_town = models.CharField(
        verbose_name='住所(町域)',
        max_length=191,
        default=''
    )

    address_other = models.CharField(
        verbose_name='住所(その他)',
        max_length=191,
        default=''
    )

    phone_number = models.CharField(
        verbose_name='電話番号',
        max_length=191,
        default=''
    )

    # TODO management_tag should be relate with ShopManagementTag
    management_tags = models.ManyToManyField(
        ManagementTag,
        verbose_name='管理タグ',
        null=True
    )

    start_available_date = models.DateField(
        verbose_name='利用開始日'
    )

    end_available_date = models.DateField(
        verbose_name='利用終了日',
        null=True
    )
