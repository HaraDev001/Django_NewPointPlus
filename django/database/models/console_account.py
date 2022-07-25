import uuid

from django.db import models

from .common.models import CommonModel


class ConsoleAccount(CommonModel):

    class Meta:
        db_table = 'console_account'
        verbose_name = verbose_name_plural = '管理コンソールアカウント情報'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    provider = models.ForeignKey(
        'database.Provider',
        verbose_name='事業者ID',
        on_delete=models.SET_NULL,
        null=True  # TODO: temporary set NULL since not sure about provider data
    )

    email = models.EmailField(
        verbose_name='業種名',
        max_length=255
    )

    group = models.ForeignKey(
        'database.Group',
        verbose_name='',
        on_delete=models.PROTECT,
    )

    role = models.ForeignKey(
        'database.Role',
        verbose_name='',
        on_delete=models.PROTECT,
    )
