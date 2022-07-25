from django.db import models

from .common.models import CommonModel


class Prefectures(CommonModel):
    class Meta:
        db_table = 'prefectures'
        verbose_name = verbose_name_plural = '都道府県情報'

    id = models.AutoField(
        primary_key=True,
        verbose_name='都道府県ID',
        editable=False
    )

    name = models.CharField(
        verbose_name='都道府県名',
        max_length=5
    )
