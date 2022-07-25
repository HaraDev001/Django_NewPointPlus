from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer
from drf_spectacular.utils import OpenApiExample

from database.models import Card, Transaction


class StatusSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=200)
    message = serializers.CharField(max_length=200)


class CommonSerializer(serializers.Serializer):
    status = StatusSerializer()


class OpenApiAccessTokenIssueSerializer(serializers.Serializer):
    auth_token = serializers.CharField(default='認証トークン')
    token_expiration_date = serializers.DateTimeField()
    refresh_token = serializers.CharField(default='リフレッシュトークン')


class OpenApiAccessTokenUpdateSerializer(serializers.Serializer):
    auth_token = serializers.CharField(default='認証トークン')
    token_expiration_date = serializers.DateTimeField()
    refresh_token = serializers.CharField(default='リフレッシュトークン')


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Success',
            summary='Success',
            value={
                'card_config_name': 'カード設定名',
                'card_design': 1,
                'card_number': 'カード番号',
                'status': 1,
                # 1日あたりのチャージ上限額(チャージ可能額(日))
                'value_charge_limit_for_day': 1,
                # 1ヶ月あたりのチャージ上限額(チャージ可能額(月))
                'value_charge_limit_for_month': 1,
                # 1日あたりの決済上限額
                'value_payment_limit_for_day': 1,
                # 1ヶ月あたりの決済上限額
                'value_payment_limit_for_month': 1,
                # 1日のチャージ実績額
                'actual_amount_charge_limit_for_day': 1,
                # 1ヶ月のチャージ実績額
                'actual_amount_charge_limit_for_month': 1,
                # 1日の決済実績額
                'actual_amount_payment_limit_for_day': 1,
                # 1ヶ月あたりの決済実績額
                'actual_amount_payment_limit_for_month': 1,
            },
            response_only=True,
            status_codes=['200']
        )
    ]
)
class OpenApiCardDetailSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Card


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Success',
            summary='Success',
            value={
                'payable_available_total_balance': 1,
                'balance': {
                    'value': {
                        'total_balance': '前払バリュー合計残高',
                        'usage_restriction': [{
                            'usage_restriction_pattern': 1,
                            'usage_restriction_balance': '前払バリュー利用制限別残高',
                            'restricted_company': [{
                                'corporate_number': '前払バリュー制限対象企業番号',
                                'name': '前払バリュー制限対象企業名',
                            }],
                            'restricted_shop': [{
                                'shop_number': '前払バリュー制限対象店舗番号',
                                'name': '前払バリュー制限対象店舗名',
                            }],
                            'expiration': [{
                                'expired_on': '前払バリュー有効期限日',
                                'expired_on_balance': '前払バリュー有効期限別残高',
                            }]
                        }]
                    },
                    'payable_bonus': {
                        'total_balance': '決済併用ボーナス合計残高',
                        'usage_restriction': [{
                            'usage_restriction_pattern': 1,
                            'usage_restriction_balance': '決済併用ボーナス利用制限別残高',
                            'restricted_company': [{
                                'corporate_number': '決済併用ボーナス制限対象企業番号',
                                'name': '決済併用ボーナス制限対象企業名',
                            }],
                            'restricted_shop': [{
                                'shop_number': '決済併用ボーナス制限対象店舗番号',
                                'name': '決済併用ボーナス制限対象店舗名',
                            }],
                            'expiration': [{
                                'expired_on': '決済併用ボーナス有効期限日',
                                'expired_on_balance': '決済併用ボーナス有効期限別残高',
                            }]
                        }]
                    },
                    'exchange_bonus': {
                        'total_balance': '商品交換ボーナス合計残高',
                        'usage_restriction': [{
                            'usage_restriction_pattern': '商品交換ボーナス利用制限パターン',
                            'usage_restriction_balance': '商品交換ボーナス利用制限別残高',
                            'restricted_company': [{
                                'corporate_number': '商品交換ボーナス制限対象企業番号',
                                'name': '商品交換ボーナス制限対象企業名',
                            }],
                            'restricted_shop': [{
                                'shop_number': '商品交換ボーナス制限対象店舗番号',
                                'name': '商品交換ボーナス制限対象店舗名',
                            }],
                            'expiration': [{
                                'expired_on': '商品交換ボーナス有効期限日',
                                'expired_on_balance': '商品交換ボーナス有効期限別残高',
                            }]
                        }]
                    },
                },
                'reserve_balance': {
                    'value': [{
                        'grant_on': '前払バリュー付与予定日',
                        'grant_amount': '前払バリュー付与予定数',
                        'usage_restriction_pattern': 1,
                        'restricted_company': [{
                            'corporate_number': '前払バリュー制限対象企業番号',
                            'name': '前払バリュー制限対象企業名',
                        }],
                        'restricted_shop': [{
                            'shop_number': '前払バリュー制限対象店舗番号',
                            'name': '前払バリュー制限対象店舗名',
                        }],
                    }],
                    'payable_bonus': [{
                        'grant_on': '決済併用ボーナス付与予定日',
                        'grant_amount': '決済併用ボーナス付与予定数',
                        'usage_restriction_pattern': 1,
                        'restricted_company': [{
                            'corporate_number': '決済併用ボーナス制限対象企業番号',
                            'name': '決済併用ボーナス制限対象企業名',
                        }],
                        'restricted_shop': [{
                            'shop_number': '決済併用ボーナス制限対象店舗番号',
                            'name': '決済併用ボーナス制限対象店舗名',
                        }],
                    }],
                    'exchange_bonus': [{
                        'grant_on': '商品交換ボーナス付与予定日',
                        'grant_amount': '商品交換ボーナス付与予定数',
                        'usage_restriction_pattern': '商品交換ボーナス利用制限パターン',
                        'restricted_company': [{
                            'corporate_number': '商品交換ボーナス制限対象企業番号',
                            'name': '商品交換ボーナス制限対象企業名',
                        }],
                        'restricted_shop': [{
                            'shop_number': '商品交換ボーナス制限対象店舗番号',
                            'name': '商品交換ボーナス制限対象店舗名',
                        }],
                    }]
                }
            },
            response_only=True,
            status_codes=['200']
        )
    ]
)
class OpenApiCardBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Card


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Success',
            summary='Success',
            value={
                'replacement_value': 1,
                'replacement_payable_bonus': 1,
                'replacement_exchange_bonus': 1,
                'source': {
                    'card_config_name':  '付替元カード設定名',
                    'card_number': '付替元カード番号',
                    'before_value_balance': '付替元前払バリュー残高',
                    'before_value_expired_on': '付替元前払バリュー有効期限日',
                    'before_payable_bonus_balance': '付替元決済併用ボーナス残高',
                    'before_exchange_bonus_balance': '付替元商品交換ボーナス残高',
                    'after_value_balance': '付替元前払バリュー残高',
                    'after_value_expired_on': '付替元前払バリュー有効期限日',
                    'after_payable_bonus_balance': '付替元決済併用ボーナス残高',
                    'after_exchange_bonus_balance': '付替元商品交換ボーナス残高'
                },
                'target': {
                    'card_config_name': '付替先カード設定名',
                    'card_number': '付替先カード番号',
                    'before_value_balance': '付替先前払バリュー残高',
                    'before_value_expired_on': '付替先前払バリュー有効期限日',
                    'before_payable_bonus_balance': '付替先決済併用ボーナス残高',
                    'before_exchange_bonus_balance': '商品交換ボーナス残高',
                    'after_value_balance': '前払バリュー残高',
                    'after_value_expired_on': '前払バリュー有効期限日',
                    'after_payable_bonus_balance': '決済併用ボーナス残高',
                    'after_exchange_bonus_balance': '商品交換ボーナス残高',
                }
            },
            response_only=True,
            status_codes=['200']
        )
    ]
)
class OpenApiCardReplaceSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Card


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Success',
            summary='Success',
            value={
                'transaction_number': 1,
            },
            response_only=True,
            status_codes=['200']
        )
    ]
)
class OpenApiIssueTransactionNumberSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Transaction


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Success',
            summary='Success',
            value={
                'transaction_number': 1,
                'transaction_type': 1,
                'transaction_at': 11,
                'corporate_number': '企業番号',
                'company_name': '企業名',
                'shop_number': '店舗番号',
                'shop_name': '店舗名',
                'terminal_number': '端末番号',
                'charge_amount': 'チャージ額',
                'card_transaction': [
                    {
                        'card_config_name': 'カード設定名',
                        'card_number': 'カード番号',
                        'before_value_balance': '取引前前払バリュー残高',
                        'before_value_expired_at': '取引前前払バリュー有効期限',
                        'before_payable_bonus_balance': '取引前決済併用ボーナス残高',
                        'before_exchange_bonus_balance': '取引前商品交換ボーナス残高',
                        'after_value_balance': '取引後前払バリュー残高',
                        'after_value_expired_at': '取引後前払バリュー有効期限',
                        'after_payable_bonus_balance': '取引後決済併用ボーナス残高',
                        'after_exchange_bonus_balance': '取引後商品交換ボーナス残高',
                        'apply_campaign': [
                            {
                                'campaign_name': 'キャンペーン名',
                                'bonus_category': 'ボーナス種別',
                                'bonus_grant_amount': 'ボーナス付与数',
                                'bonus_expired_at': 'ボーナス有効期限日',
                                'bonus_reserve_grant_at': 'キャンペーン付与予定日'
                            }
                        ]
                    }
                ],
            },
            response_only=True,
            status_codes=['200']
        )
    ]
)
class OpenApiTransactionChargeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Transaction


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Success',
            summary='Success',
            value={
                'transaction_number': 1,
                'transaction_type': 1,
                'transaction_at': 11,
                'corporate_number': '企業番号',
                'company_name': '企業名',
                'shop_number': '店舗番号',
                'shop_name': '店舗名',
                'terminal_number': '端末番号',
                'used_total_amount': '決済額',
                'used_value_amount': '前払バリュー利用額',
                'used_payable_bonus_amount': '決済併用ボーナス利用数',
                'card_transaction': [
                    {
                        'card_config_name': 'カード設定名',
                        'card_number': 'カード番号',
                        'before_value_balance': '取引前前払バリュー残高',
                        'before_value_expired_at': '取引前前払バリュー有効期限',
                        'before_payable_bonus_balance': '取引前決済併用ボーナス残高',
                        'before_exchange_bonus_balance': '取引前商品交換ボーナス残高',
                        'after_value_balance': '取引後前払バリュー残高',
                        'after_value_expired_at': '取引後前払バリュー有効期限',
                        'after_payable_bonus_balance': '取引後決済併用ボーナス残高',
                        'after_exchange_bonus_balance': '取引後商品交換ボーナス残高',
                        'apply_campaign': [
                            {
                                'campaign_name': 'キャンペーン名',
                                'bonus_category': 'ボーナス種別',
                                'bonus_grant_amount': 'ボーナス付与数',
                                'bonus_expired_at': 'ボーナス有効期限日',
                                'bonus_reserve_grant_at': 'キャンペーン付与予定日'
                            }
                        ]
                    }
                ],

            },
            response_only=True,
            status_codes=['200']
        )
    ]
)
class OpenApiTransactionPaySerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Transaction


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Success',
            summary='Success',
            value={
                'transaction_number': 1,
                'transaction_type': 1,
                'transaction_at': 11,
                'corporate_number': '企業番号',
                'company_name': '企業名',
                'shop_number': '店舗番号',
                'shop_name': '店舗名',
                'terminal_number': '端末番号',
                'grant_method': '付与方法',
                'grant_category': '種別',
                'grant_amount': '付与数',
                'grant_expired_at': '有効期限日',
                'card_transaction': [
                    {
                        'card_config_name': 'カード設定名',
                        'card_number': 'カード番号',
                        'before_payable_bonus_balance': '取引前決済併用ボーナス残高',
                        'before_exchange_bonus_balance': '取引前商品交換ボーナス残高',
                        'after_payable_bonus_balance': '取引後決済併用ボーナス残高',
                        'after_exchange_bonus_balance': '取引後商品交換ボーナス残高',
                        'apply_campaign': [
                            {
                                'campaign_name': 'キャンペーン名',
                                'bonus_category': 'ボーナス種別',
                                'bonus_grant_amount': 'ボーナス付与数',
                                'bonus_expired_at': 'ボーナス有効期限日',
                                'bonus_reserve_grant_at': 'キャンペーン付与予定日'
                            }
                        ]
                    }
                ],
            },
            response_only=True,
            status_codes=['200']
        )
    ]
)
class OpenApiTransactionGrantSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Transaction


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Success',
            summary='Success',
            value={
                'transaction_number': 1,
                'transaction_type': 1,
                'transaction_at': 11,
                'corporate_number': '企業番号',
                'company_name': '企業名',
                'shop_number': '店舗番号',
                'shop_name': '店舗名',
                'terminal_number': '端末番号',
                'used_amount': 'ボーナス利用数',
                'card_transaction': [
                    {
                        'card_config_name': 'カード設定名',
                        'card_number': 'カード番号',
                        'before_exchange_bonus_balance': '取引前商品交換ボーナス残高',
                        'after_exchange_bonus_balance': '取引後商品交換ボーナス残高',
                        'apply_campaign': [
                            {
                                'campaign_name': 'キャンペーン名',
                                'bonus_category': 'ボーナス種別',
                                'bonus_grant_amount': 'ボーナス付与数',
                                'bonus_expired_at': 'ボーナス有効期限日',
                                'bonus_reserve_grant_at': 'キャンペーン付与予定日'
                            }
                        ]
                    }
                ],
            },
            response_only=True,
            status_codes=['200']
        )
    ]
)
class OpenApiTransactionUseSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Transaction


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Success',
            summary='Success',
            value={
                'transaction_type': 1,
                'transaction_at': 11,
                'corporate_number': '企業番号',
                'company_name': '企業名',
                'shop_number': '店舗番号',
                'shop_name': '店舗名',
                'terminal_number': '端末番号',
                'terminal_type': '端末種別',
                'transaction_cancel_total_amount': '取消取引額',
                'transaction_cancel_value_amount': '取引取消前払バリュー増減額',
                'transaction_cancel_payable_bonus_amount': '取引取消決済併用ボーナス増減数',
                'transaction_cancel_exchange_bonus_amount': '取引取消商品交換ボーナス増減数',
                'card_transaction': [
                    {
                        'card_config_name': 'カード設定名',
                        'card_number': 'カード番号',
                        'before_value_balance': '取引前前払バリュー残高',
                        'before_value_expired_at': '取引前前払バリュー有効期限日',
                        'before_payable_bonus_balance': '取引前決済併用ボーナス残高',
                        'before_exchange_bonus_balance': '取引前商品交換ボーナス残高',
                        'after_value_balance': '取引後前払バリュー残高',
                        'after_value_expired_at': '取引後前払バリュー有効期限日',
                        'after_payable_bonus_balance': '取引後決済併用ボーナス残高',
                        'after_exchange_bonus_balance': '取引後商品交換ボーナス残高',
                        'apply_campaign': [
                            {
                                'campaign_name': 'キャンペーン名',
                                'bonus_category': 'ボーナス種別',
                                'bonus_grant_amount': 'ボーナス付与数',
                                'bonus_expired_at': 'ボーナス有効期限日',
                                'bonus_reserve_grant_at': 'キャンペーン付与予定日'
                            }
                        ]
                    }
                ],
            },
            response_only=True,
            status_codes=['200']
        )
    ]
)
class OpenApiTransactionCancelSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Transaction


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Success',
            summary='Success',
            value=[
                {
                    'transaction_type': 1,
                    'transaction_at': 11,
                    'transaction_number': '取引番号',
                    'transaction_status': 1,
                    'transaction_total_amount': '取引総額',
                    'corporate_number': '企業番号',
                    'company_name': '企業名',
                    'shop_number': '店舗番号',
                    'shop_name': '店舗名',
                    'terminal_number': '端末番号',
                    'terminal_type': '端末種別',
                    'card': [
                        {
                            'card_number': 'カード番号',
                            'card_config_name': 'カード設定名',
                            'card_config_category': 'カード設定種別'
                        }
                    ],
                    'apply_campaign': [
                        {
                            'campaign_name': 'キャンペーン名',
                            'bonus_grant_amount': 'ボーナス付与合計数',
                            'bonus_grant_at': 'ボーナス付与日時',
                        }
                    ]
                }
            ],
            response_only=True,
            status_codes=['200']
        )
    ]
)
class OpenApiTransactionListSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Transaction


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Success',
            summary='Success',
            value={
                'transaction_type': 1,
                'transaction_at': 11,
                'transaction_number': '取引番号',
                'transaction_status': 1,
                'transaction_total_amount': '取引額',
                'transaction_value_amount': '取引前払バリュー増減額',
                'transaction_payable_bonus_amount': '取引決済併用ボーナス増減数',
                'transaction_exchange_bonus_amount': '取引商品交換ボーナス増減数',
                'corporate_number': '企業番号',
                'company_name': '企業名',
                'shop_number': '店舗番号',
                'shop_name': '店舗名',
                'terminal_number': '端末番号',
                'terminal_type': '端末種別',
                'card_transaction': [
                    {
                        'card_number': 'カード番号',
                        'card_config_name': 'カード設定名',
                        'card_config_category': 'カード設定種別',
                        'card_value_amount': 'カード前払バリュー増減額',
                        'card_payable_bonus_amount': 'カード決済併用ボーナス増減数',
                        'card_exchange_bonus_amount': 'カード商品交換ボーナス増減数',
                        'replacement_source_card_number': '付替元カード番号',
                        'replacement_source_card_config_name': '付替元カード設定名',
                        'replacement_target_card_number': '付替先カード番号',
                        'replacement_target_card_config_name': '付替先カード設定名',
                        'apply_campaign': [
                            {
                                'campaign_name': 'キャンペーン名',
                                'bonus_category': 'ボーナス種別',
                                'bonus_grant_amount': 'ボーナス付与数',
                                'bonus_expired_at': 'ボーナス有効期限日',
                                'bonus_reserve_grant_at': 'キャンペーン付与予定日'
                            }
                        ],
                    }
                ]
            },
            response_only=True,
            status_codes=['200']
        )
    ]
)
class OpenApiTransactionDetailASerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Transaction


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Success',
            summary='Success',
            value={
                'charge': {
                    'charge_total_amount': 'チャージ合計額',
                    'charge_total_count': 'チャージ合計件数',
                    'charge_cancel_total_amount': 'チャージ取消合計額',
                    'charge_cancel_total_count': 'チャージ取消合計件数'
                },
                'payment': {
                    'total_amount': '決済合計額',
                    'total_count': '決済合計件数',
                    'cancel_total_amount': '決済取消合計額',
                    'cancel_total_count': '決済取消合計件数',
                    'value_total_amount': '前払バリュー合計額',
                    'value_cancel_total_amount': '前払バリュー取消合計額',
                    'payable_bonus_total_amount': '決済併用ボーナス合計額',
                    'payable_bonus_cancel_total_amount': '決済併用ボーナス取消合計額',
                },
                'grant': {
                    'payable_bonus_total_amount': '決済併用ボーナス付与合計額',
                    'payable_bonus_total_count': '決済併用ボーナス付与合計件数',
                    'payable_bonus_cancel_total_amount': '決済併用ボーナス付与取消合計額',
                    'payable_bonus_cancel_total_count': '決済併用ボーナス付与取消合計件数',
                    'exchange_bonus_total_amount': '商品交換ボーナス付与合計額',
                    'exchange_bonus_total_count': '商品交換ボーナス付与合計件数',
                    'exchange_bonus_cancel_total_amount': '商品交換ボーナス付与取消合計額',
                    'exchange_bonus_cancel_total_count': '商品交換ボーナス付与取消合計件数',
                },
                'used': {
                    'exchange_bonus_total_amount': '商品交換ボーナス合計額利用',
                    'exchange_bonus_total_count': '商品交換ボーナス合計件数利用',
                    'exchange_bonus_cancel_total_amount': '商品交換ボーナス取消合計額利用',
                    'exchange_bonus_cancel_total_count': '商品交換ボーナス取消合計件数利用',
                }
            },
            response_only=True,
            status_codes=['200']
        )
    ]
)
class OpenApiTransactionSummarySerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Transaction
