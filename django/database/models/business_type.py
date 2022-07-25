from django.db import models
import uuid

from .common.models import CommonModel


class BusinessType(CommonModel):

    class Meta:
        db_table = 'business_type'
        verbose_name = verbose_name_plural = '業種情報'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    business_type_name = models.CharField(
        verbose_name='業種名',
        max_length=191,
        default=''
    )
