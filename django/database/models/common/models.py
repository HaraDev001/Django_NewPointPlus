from django.db import models


class CommonModel(models.Model):
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)

    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    class Meta:
        abstract = True
