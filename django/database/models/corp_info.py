from django.db import models
import uuid

from .common.models import CommonModel


class CorpInfo(CommonModel):

    class Meta:
        db_table = 'corp_info'
        verbose_name = verbose_name_plural = 'サービス情報'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    host = models.CharField(
        verbose_name='ホスト名',
        max_length=191,
        default=''
    )

    company_name = models.CharField(
        verbose_name='事業者名',
        max_length=191,
        default=''
    )

    service_name = models.CharField(
        verbose_name='サービス名',
        max_length=191,
        default=''
    )

    logo_url = models.URLField(
        verbose_name='事業者サービスロゴURL',
        default=''
    )

    privacy_policy_url = models.URLField(
        verbose_name='プライバシーポリシーURL',
        default=''
    )

    privacy_policy_regulation_date = models.DateTimeField(
        verbose_name='プライバシーポリシー規定日'
    )

    privacy_policy_version = models.CharField(
        verbose_name='プライバシーポリシーバージョン ',
        max_length=191,
        null=True
    )

    terms_of_service_url = models.URLField(
        verbose_name='利用規約URL',
        default=''
    )

    terms_of_service_regulation_date = models.DateTimeField(
        verbose_name='利用規約規定日'
    )

    terms_of_service_version = models.CharField(
        verbose_name='利用規約バージョン',
        max_length=191,
        default=''
    )

    copyright_notice = models.CharField(
        verbose_name='著作権表示',
        max_length=191,
        default=''
    )

    e_money_card = models.IntegerField(
        verbose_name='電子マネーカード可否',
        default=0
    )

    prepaid_value = models.IntegerField(
        verbose_name='前払バリュー可否',
        default=0
    )

    payable_bonus = models.IntegerField(
        verbose_name='決済併用ボーナス可否',
        default=0
    )

    exchange_bonus = models.IntegerField(
        verbose_name='商品交換ボーナス可否',
        default=0
    )