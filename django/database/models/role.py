import uuid

from django.db import models

from .common.models import CommonModel


class Role(CommonModel):
    class Meta:
        db_table = 'role'
        verbose_name = verbose_name_plural = ''  # TODO

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    name = models.CharField(
        verbose_name='',
        max_length=255,
    )
