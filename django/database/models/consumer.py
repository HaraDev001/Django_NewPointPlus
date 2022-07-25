import uuid

from django.db import models

from .common.models import CommonModel


class Consumer(CommonModel):
    INUSE = 0
    LOGIN_LOCK = 1
    SUSPENDED = 2
    WITHDRAWN = 3
    STATUS_CHOICES = (
        (INUSE, '利用中'),
        (LOGIN_LOCK, 'ログインロック'),
        (SUSPENDED, '利用停止'),
        (WITHDRAWN, '退会済み'),
    )

    MALE = 0
    FEMALE = 1
    OTHER = 2
    GENDER_CHOICES = (
        (MALE, '男'),
        (FEMALE, '女'),
        (OTHER, 'その他'),
    )

    class Meta:
        db_table = 'consumer'
        verbose_name = verbose_name_plural = '消費者アカウント情報'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    provider = models.ForeignKey(
        'database.Provider',
        verbose_name='事業者ID',
        on_delete=models.PROTECT
    )

    status = models.IntegerField(
        verbose_name='アカウント状態',
        choices=STATUS_CHOICES
    )

    consumer_number = models.CharField(
        verbose_name='会員番号',
        max_length=255
    )

    email = models.CharField(
        verbose_name='メールアドレス',
        max_length=255,
        default=''
    )

    user_name = models.CharField(
        verbose_name='氏名',
        max_length=255,
        default=''
    )

    user_phonetic_name = models.CharField(
        verbose_name='氏名カナ',
        max_length=255,
        default=''
    )

    nickname = models.CharField(
        verbose_name='ニックネーム',
        max_length=255,
        null=True
    )

    phone_number = models.CharField(
        verbose_name='電話番号',
        max_length=255,
        default=''
    )

    birthday = models.DateField(
        verbose_name='生年月日'
    )

    country = models.CharField(
        verbose_name='国籍',
        max_length=255,
        default=''
    )

    address_pref = models.CharField(
        verbose_name='住所(都道府県)',
        max_length=255,
        default=''

    )

    address_city = models.CharField(
        verbose_name='住所(市区町村)',
        max_length=255,
        default=''
    )

    address_town = models.CharField(
        verbose_name='住所(町域)',
        max_length=255,
        default=''
    )

    address_other = models.CharField(
        verbose_name='住所(その他)',
        max_length=255,
        default=''
    )

    gender = models.IntegerField(
        verbose_name='性別',
        choices=GENDER_CHOICES,
        default=MALE
    )

    profession = models.CharField(
        verbose_name='職業',
        max_length=255,
        default=''
    )

    news_notification_enabled = models.BooleanField(
        verbose_name='お知らせ通知可否',
        default=True
    )
