import uuid

from django.db import models

from .common.models import CommonModel
from .common.choices import CardStatus


class Card(CommonModel):

    class Meta:
        db_table = 'card'
        ordering = ['card_number']
        verbose_name = verbose_name_plural = 'カード情報'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    card_config = models.ForeignKey(
        'database.CardConfig',
        verbose_name='カード設定ID',
        on_delete=models.PROTECT
    )

    consumer = models.ForeignKey(
        'database.Consumer',
        verbose_name='消費者アカウントID',
        null=True,
        on_delete=models.SET_NULL
    )

    card_number = models.CharField(
        verbose_name='カード番号',
        unique=True,
        max_length=24
    )

    # TODO: 暗号化後の文字数によってTextFieldも視野に入れる
    pin_number = models.CharField(
        verbose_name='PIN番号',
        max_length=191
    )

    magnetic_information = models.CharField(
        verbose_name='磁気情報',
        unique=True,
        max_length=69,
        null=True
    )

    status = models.IntegerField(
        verbose_name='カード状態',
        choices=CardStatus.choices,
        default=CardStatus.NOT_ACTIVATED
    )

    activated_at = models.DateTimeField(
        verbose_name='アクティベート日時',
        null=True
    )

    destroyed_at = models.DateTimeField(
        verbose_name='破棄日時',
        null=True
    )

    is_locked = models.BooleanField(
        verbose_name='ロックフラグ',
        default=False
    )

    is_test = models.BooleanField(
        verbose_name='テストカードフラグ',
        default=False
    )

    remarks = models.TextField(
        verbose_name='備考',
        max_length=255,
        null=True
    )

