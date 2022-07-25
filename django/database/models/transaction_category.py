from django.db import models
import uuid

from .common.models import CommonModel


class TransactionCategory(CommonModel):

    class Meta:
        db_table = 'transaction_category'
        verbose_name = verbose_name_plural = '取引種別情報'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    name = models.CharField(
        verbose_name='取引種別名',
        max_length=191,
        default=''
    )
