import uuid

from django.db import models

from .common.models import CommonModel
from .common.choices import ManagementTagCategory


class ManagementTag(CommonModel):

    class Meta:
        db_table = 'management_tag'
        verbose_name = verbose_name_plural = '管理タグ情報'
        ordering = ["name", ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    name = models.CharField(
        verbose_name='管理タグ名',
        max_length=191,
        default=''
    )

    category = models.IntegerField(
        verbose_name='管理タグ種別',
        choices=ManagementTagCategory.choices
    )
