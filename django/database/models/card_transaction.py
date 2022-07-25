import uuid

from django.db import models

from .common.models import CommonModel
from .common.choices import TransactionCategory


class CardTransaction(CommonModel):

    class Meta:
        db_table = 'card_transaction'
        verbose_name = verbose_name_plural = 'カード取引履歴情報'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    transaction = models.ForeignKey(
        'database.Transaction',
        verbose_name='取引ID',
        on_delete=models.CASCADE
    )

    transaction_at = models.DateTimeField(
        verbose_name='カード取引日時',
    )

    transaction_type = models.IntegerField(
        verbose_name='カード取引種別',
        choices=TransactionCategory.choices
    )

    card = models.ForeignKey(
        'database.Card',
        verbose_name='カードID',
        on_delete=models.CASCADE
    )

    card_config = models.ForeignKey(
        'database.CardConfig',
        verbose_name='カード設定id',
        on_delete=models.SET_NULL,
        null=True
    )

    provider = models.ForeignKey(
        'database.Provider',
        verbose_name='事業者ID',
        on_delete=models.CASCADE
    )

    company = models.ForeignKey(
        'database.Company',
        verbose_name='企業ID',
        max_length=32,
        on_delete=models.SET_NULL,
        null=True
    )

    shop = models.ForeignKey(
        'database.Shop',
        verbose_name='店舗ID',
        max_length=32,
        on_delete=models.SET_NULL,
        null=True
    )

    terminal = models.ForeignKey(
        'database.Terminal',
        verbose_name='店舗端末ID',
        max_length=32,
        on_delete=models.SET_NULL,
        null=True
    )

    prepaid_value = models.IntegerField(
        verbose_name='前払いバリュー取引額',
        default=0
    )

    payable_bonus = models.IntegerField(
        verbose_name='決済併用ボーナス取引数',
        default=0
    )

    exchange_bonus = models.IntegerField(
        verbose_name='商品交換ボーナス取引数',
        default=0
    )

    replace_source_card_number = models.CharField(
        verbose_name='付替元カード番号',
        max_length=24,
        null=True
    )

    replace_target_card_number = models.CharField(
        verbose_name='付替先カード番号',
        max_length=24,
        null=True
    )

    grant_value = models.ForeignKey(
        'database.Value',
        verbose_name='付与バリューID',
        max_length=32,
        on_delete=models.SET_NULL,
        null=True
    )

    grant_bonus = models.ForeignKey(
        'database.Bonus',
        verbose_name='付与ボーナスID',
        max_length=32,
        on_delete=models.SET_NULL,
        null=True
    )
