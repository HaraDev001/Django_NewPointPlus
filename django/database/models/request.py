import uuid

from django.db import models

from .common.models import CommonModel


class Request(CommonModel):

    class Meta:
        db_table = 'request'
        verbose_name = verbose_name_plural = '申請情報'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    requested_at = models.DateTimeField(
        verbose_name='申請日時'
    )

    request_category = models.IntegerField(
        verbose_name='申請種別'
    )

    request_status = models.IntegerField(
        verbose_name='申請ステータス'
    )

    request_account = models.ForeignKey(
        'database.ConsoleAccount',
        on_delete=models.CASCADE,
        related_name='request_account',
        db_column='request_account',
    )

    approve_account = models.ForeignKey(
        'database.ConsoleAccount',
        on_delete=models.CASCADE,
        related_name='approve_account',
        db_column='approve_account',
        null=True
    )

    transaction = models.ForeignKey(
        'database.Transaction',
        on_delete=models.CASCADE,
        null=True
    )
