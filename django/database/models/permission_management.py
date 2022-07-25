import uuid

from database.models.common.const import STATE_CHOICE
from database.models.common.models import CommonModel

from django.db import models


class PermissionManagement(CommonModel):

    class Meta:
        db_table = 'permission_management'
        verbose_name = verbose_name_plural = ''  # TODO

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    group = models.ForeignKey(
        'database.Group',
        verbose_name='',
        on_delete=models.CASCADE,
    )

    role = models.ForeignKey(
        'database.Role',
        verbose_name='',
        on_delete=models.CASCADE,
    )

    permission = models.ForeignKey(
        'database.Permission',
        verbose_name='',
        on_delete=models.CASCADE,
    )

    state = models.IntegerField(
        choices=STATE_CHOICE
    )

    remarks = models.TextField(
        default=''
    )
