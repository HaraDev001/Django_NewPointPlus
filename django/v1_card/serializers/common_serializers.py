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
                'card_number': 'カード番号',
                'card_status': 1,
                'card_design': 'カードデザイン(S3のURL)',
                'card_config_name': 'カード設定名',
                'value_charge_limit_for_day': 1,
                'value_charge_limit_for_month': 1,
                'value_payment_limit_for_day': 1,
                'value_payment_limit_for_month': 1,
                'value_currency_unit': '前払いバリュー通貨単位',
                'payable_bonus_currency_unit': '決済併用ボーナス通貨単位',
                'exchange_bonus_currency_unit': '商品交換ボーナス通貨単位',
                'actual_amount_charge_for_day': 1,
                'actual_amount_charge_for_month': 1,
                'actual_amount_payment_for_day': 1,
                'actual_amount_payment_for_month': 1,
            },
            response_only=True,
            status_codes=['200']
        )
    ]
)
class OpenApiCardDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = "__all__"


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
                                'expired_at': '前払バリュー有効期限日',
                                'expired_at_balance': '前払バリュー有効期限別残高',
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
                                'expired_at': '決済併用ボーナス有効期限日',
                                'expired_at_balance': '決済併用ボーナス有効期限別残高',
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
                                'expired_at': '商品交換ボーナス有効期限日',
                                'expired_at_balance': '商品交換ボーナス有効期限別残高',
                            }]
                        }]
                    },
                },
                'reserve_balance': {
                    'value': [{
                        'grant_at': '前払バリュー付与予定日',
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
                        'grant_at': '決済併用ボーナス付与予定日',
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
                        'grant_at': '商品交換ボーナス付与予定日',
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
class OpenApiBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = "__all__"


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Success',
            summary='Success',
            value=[{
                'transaction_type': 1,
                'transaction_number': 1,
                'transaction_status': 1,
                'transaction_at': 1,
                'transaction_value_increase_decrease_amount': '取引前払バリュー増減額',
                'transaction_payable_bonus_increase_decrease_amount': '取引決済併用ボーナス増減数',
                'transaction_product_exchange_bonus_increase_decrease_amount': '取引商品交換ボーナス増減数',
                'replacement_source_card_config_name': '付替元カード設定名',
                'replacement_target_card_config_name': '付替先カード設定名',
                'apply_campaign': [
                    {
                        'bonus_category': 'ボーナス種別',
                        'bonus_grant_amount': 'ボーナス付与数',
                        'bonus_reserve_grant_at': 'キャンペーン付与予定日'
                    }
                ],
            }],
            response_only=True,
            status_codes=['200']
        )
    ]
)
class OpenApiTransactionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Success',
            summary='Success',
            value={
                'transaction_type': 1,
                'transaction_number': 1,
                'transaction_status': 1,
                'transaction_at': 1,
                'transaction_value_increase_decrease_amount': '取引前払バリュー増減額',
                'transaction_payable_bonus_increase_decrease_amount': '取引決済併用ボーナス増減数',
                'transaction_product_exchange_bonus_increase_decrease_amount': '取引商品交換ボーナス増減数',
                'replacement_source_card_number': '付替元カード番号',
                'replacement_source_card_config_name': '付替元カード設定名',
                'replacement_source_card_design_url': '付替元カードデザインURL',
                'replacement_target_card_number': '付替先カード番号',
                'replacement_target_card_config_name': '付替先カード設定名',
                'replacement_target_card_design_url': '付替先カードデザインURL',
                'apply_campaign': [
                    {
                        'bonus_category': 'ボーナス種別',
                        'bonus_grant_amount': 'ボーナス付与数',
                        'bonus_reserve_grant_at': 'キャンペーン付与予定日'
                    }
                ],
            },
            response_only=True,
            status_codes=['200']
        )
    ]
)
class OpenApiTransactionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Success',
            summary='Success',
            value={
                'provider_name': '事業者名',
                'service_name': 'サービス名',
                'service_logo_url': '事業者サービスロゴURL',
                'use_service': {
                    # 電子マネーカード利用可否
                    'is_physical_card_enable': True
                },
                'use_account': {
                    # 前払いバリュー利用可否
                    'is_value_enable': True,
                    # 決済併用ボーナス利用可否
                    'is_payable_bonus_enable': True,
                    # 商品交換ボーナス利用可否
                    'is_exchange_bonus_enable': True,
                },
                'terms_of_service': {
                    'url': '利用規約URL',
                    'regulation_date': '利用規約規定日',
                    'version': '利用規約バージョン'
                },
                'privacy_policy': {
                    'url': 'プライバシーポリシーURL',
                    'regulation_date': 'プライバシーポリシー規定日',
                    'version': 'プライバシーポリシーバージョン'
                }
            },
            response_only=True,
            status_codes=['200']
        )
    ]
)
class OpenApiInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = "__all__"
