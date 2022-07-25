import uuid

from database.models.common.models import CommonModel

from django.db import models


class Provider(CommonModel):
    UNDER_REVIEW = 1
    AVAILABLE = 2
    UNAVAILABLE = 3
    STATUS_CHOICES = (
        (UNDER_REVIEW, "審査中"),
        (AVAILABLE, "利用可"),
        (UNAVAILABLE, "退会済"),
    )

    class Meta:
        db_table = 'provider'
        verbose_name = verbose_name_plural = '事業者情報'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    owner_name = models.CharField(
        verbose_name='代表者氏名',
        max_length=191,
        default=''
    )

    owner_phonetic_name = models.CharField(
        verbose_name='代表者氏名カナ',
        max_length=191,
        default=''
    )

    owner_address_pref = models.CharField(
        verbose_name='代表者住所(都道府県)',
        max_length=191,
        default=''
    )

    owner_address_city = models.CharField(
        verbose_name='代表者住所(市区町村)',
        max_length=191,
        default=''
    )

    owner_address_town = models.CharField(
        verbose_name='代表者住所(町域名)',
        max_length=191,
        default=''
    )

    owner_address_other = models.CharField(
        verbose_name='代表者住所(その他)',
        max_length=191,
        default=''
    )

    owner_birthday = models.DateField(
        verbose_name='代表者生年月日',
        null=True
    )

    provider_name = models.CharField(
        verbose_name='事業者名称',
        max_length=191,
        default=''
    )

    provider_coporate_number = models.CharField(
        verbose_name='事業者法人番号',
        max_length=191,
        default=''
    )

    provider_postal_code = models.CharField(
        verbose_name='事業者郵便番号',
        max_length=191,
        default=''
    )

    provider_address_pref = models.CharField(
        verbose_name='事業者住所(都道府県)',
        max_length=191,
        default=''
    )

    provider_address_city = models.CharField(
        verbose_name='事業者住所(市区町村)',
        max_length=191,
        default=''
    )

    provider_address_town = models.CharField(
        verbose_name='事業者住所(町域名)',
        max_length=191,
        default=''
    )

    provider_address_other = models.CharField(
        verbose_name='事業者住所(その他)',
        max_length=191,
        default=''
    )

    provider_phone_number = models.CharField(
        verbose_name='事業者電話番号',
        max_length=191,
        default=''
    )

    inquiry_phone_number = models.CharField(
        verbose_name='事業者電話番号',
        max_length=191,
        default=''
    )

    service_name = models.CharField(
        verbose_name='サービス名称',
        max_length=191,
        default=''
    )

    service_logo_url = models.URLField(
        verbose_name='サービスロゴURL',
        default=''
    )

    start_available_date = models.DateTimeField(
        verbose_name='利用開始日',
    )

    end_available_date = models.DateTimeField(
        verbose_name='利用終了日',
        null=True
    )

    # Use in API 11-3
    value_enabled_flag = models.BooleanField(
        verbose_name='バリュー有効フラグ',  # TODO: confirm verbose_name
        default=True,
    )
    # Use in API 11-3
    physical_card_flag = models.BooleanField(
        verbose_name='物理カードフラグ',  # TODO: confirm verbose_name
        default=True,
    )
    # Use in API 11-3
    payable_bonus_flag = models.BooleanField(
        verbose_name='支払い可能ボーナスフラグ',  # TODO: confirm verbose_name
        default=True,
    )
    # Use in API 11-3
    balance_inquiry_page_flag = models.BooleanField(
        verbose_name="残高照会ページ",
        default=True,
    )
    # Use in API 11-3
    exchange_bonus_flag = models.BooleanField(
        verbose_name="残高照会ページ",
        default=True,
    )
    # Use in API 11-3
    status = models.IntegerField(
        verbose_name="ステータス",
        choices=STATUS_CHOICES,
        default=1
    )
