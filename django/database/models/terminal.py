import uuid

from django.db import models

from .common.models import CommonModel
from .common.choices import TerminalCategory

from .provider import Provider
from .company import Company
from .shop import Shop
from .management_tag import ManagementTag


class Terminal(CommonModel):

    class Meta:
        db_table = 'terminal'
        verbose_name = verbose_name_plural = '店舗端末情報'
        indexes = [
            models.Index(fields=["company", "shop", 'terminal_number']),
        ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    provider = models.ForeignKey(
        Provider,
        verbose_name='事業者ID',
        on_delete=models.CASCADE,
        default=''
    )

    company = models.ForeignKey(
        Company,
        verbose_name='企業ID',
        on_delete=models.CASCADE,
        default=''
    )

    shop = models.ForeignKey(
        Shop,
        verbose_name='店舗ID',
        on_delete=models.CASCADE,
        default=''
    )

    terminal_category = models.IntegerField(
        verbose_name='店舗端末種別',
        choices=TerminalCategory.choices,
        default=TerminalCategory.POS
    )

    terminal_number = models.CharField(
        verbose_name='店舗端末番号',
        max_length=191,
        default=''
    )

    # TODO management_tag should be relate with TerminalManagementTag
    management_tags = models.ManyToManyField(
        ManagementTag,
        verbose_name='管理タグ',
        null=True
    )

    start_available_date = models.DateField(
        verbose_name='利用開始日'
    )

    end_available_date = models.DateField(
        verbose_name='利用終了日',
        null=True
    )
