import uuid

from database.models.common.models import CommonModel
from django.db import models


class OfficialPosition(CommonModel):

    class Meta:
        db_table = 'official_position'
        verbose_name = verbose_name_plural = '店舗情報'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
    )
