from database.models import Card, Company, ManagementTag, Shop, Terminal, Transaction
from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers


class StatusSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=200)
    message = serializers.CharField(max_length=200)


class CommonSerializer(serializers.Serializer):
    status = StatusSerializer()


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Success',
            summary='Success',
            value=[
                {
                    'permission_id': '権限ID',
                    'permission_name': '権限名',
                    'permission_content': {
                        'target': '権限対象',
                        'permission': 1
                    },
                    'remarks': '備考'
                }
            ],
            response_only=True,
            status_codes=['200']
        )
    ]
)
class OpenApiOperationPermissionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = "__all__"


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Success',
            summary='Success',
            value={
                'auth_token': 'アクセストークン',
                'token_expiration_date': 'トークン有効期限',
                'refresh_token': 'リフレッシュトークン',
                'provider': [{
                    'provider_id': '事業者ID',
                    'provider_name': '事業者名',
                    'is_terms_of_service_agreed': True,
                }]
            },
            response_only=True,
            status_codes=['200']
        )
    ]
)
class OpenApiAccessTokenIssueSerializer(serializers.Serializer):
    class Meta:
        model = Shop
        fields = "__all__"


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Success',
            summary='Success',
            value={
                'auth_token': 'アクセストークン',
                'token_expiration_date': 'トークン有効期限',
                'refresh_token': 'リフレッシュトークン',
                'is_terms_of_service_agreed': True
            },
            response_only=True,
            status_codes=['200']
        )
    ]
)
class OpenApiAccessTokenUpdateSerializer(serializers.Serializer):
    class Meta:
        model = Shop
        fields = "__all__"


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Success',
            summary='Success',
            value=[
                {
                    'card_config_name': 'カード設定名',
                    'card_config_category': 'カード設定種別',
                    'card_number': 'カード番号',
                    'pin_number': 'PIN番号',
                    'magnetic_information': '磁気情報',
                    'card_status': 1,
                    'is_locked': True,
                    'is_test': True,
                    'remarks': '備考'
                }
            ],
            response_only=True,
            status_codes=['200']
        )
    ]
)
class OpenApiCardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = "__all__"


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Success',
            summary='Success',
            value={
                'card_config_name': 'カード設定名',
                'card_config_category': 'カード設定種別',
                'card_number': 'カード番号',
                'pin_number': 'PIN番号',
                'magnetic_information': '磁気情報',
                'card_status': 1,
                'is_locked': True,
                'is_test': True,
                'activated_at': 'アクティベート日時',
                'destroyed_at': '破棄日時',
                'remarks': '備考',
                'replacement_source_card_number': '付替元カード番号',
                'replacement_target_card_number': '付替先カード番号',
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
class OpenApiCardDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = "__all__"


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Success',
            summary='Success',
            value=[{
                'card_config_name': 'カード設定名',
                'card_config_category': 'カード設定種別',
                'card_number': 'カード番号',
                'pin_number': 'PIN番号',
                'magnetic_information': '磁気情報',
                'card_status': 1,
                'is_locked': True,
                'is_test': True,
                'activated_at': 'アクティベート日時',
                'destroyed_at': '破棄日時',
                'remarks': '備考',
                'replacement_source_card_number': '付替元カード番号',
                'replacement_target_card_number': '付替先カード番号',
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
            }],
            response_only=True,
            status_codes=['200']
        )
    ]
)
class OpenApiCardListCsvSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = "__all__"


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Success',
            summary='Success',
            value={
                'provider_id': 1,
                'provider_name': '1',
                'provider_status': 1,
                'provider_owner_name': '代表者名',
                'use_service': {
                    'is_physical_card_enable': True
                },
                'use_account': {
                    'is_value_enable': True,
                    'is_payable_bonus_enable': True,
                    'is_exchange_bonus_enable': True,
                },
                'use_web': {
                    'balance_inquiry_page_enable': True,
                }
            },
            response_only=True,
            status_codes=['200']
        )
    ]
)
class OpenApiProviderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = "__all__"


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Success',
            summary='Success',
            value={
                'corporate_number': '企業番号',
                'company_name': '企業名',
                'company_status': '0',
                'management_tags': [
                    '管理タグ'
                ],
                'remarks': '備考'
            },
            response_only=True,
            status_codes=['200']
        )
    ]
)
class OpenApiCompanyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Success',
            summary='Success',
            value={
                'shop_number': '店舗番号',
                'shop_name': '店舗名',
                'shop_status': 1,
                'management_tags': [
                    '管理タグ'
                ],
                'remarks': '備考'
            },
            response_only=True,
            status_codes=['200']
        )
    ]
)
class OpenApiShopListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = "__all__"


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Success',
            summary='Success',
            value={
                'terminal_type': '端末種別',
                'terminal_number': '端末番号',
                'terminal_status': 1,
                'management_tags': [
                    '管理タグ'
                ],
                'remarks': '備考'
            },
            response_only=True,
            status_codes=['200']
        )
    ]
)
class OpenApiTerminalListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Terminal
        fields = "__all__"


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
        model = Transaction
        fields = "__all__"

    def create(self, validated_data):
        transaction = Transaction(
        )
        transaction.save()
        return transaction


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Success',
            value={
                'transaction_type': {
                    'id': '取引種別id',
                    'name': '取引種別名',
                }
            },
            summary='Success',
            response_only=True,
            status_codes=['200']
        )
    ]
)
class OpenApiTransactionTypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Success',
            summary='Success',
            value=[{
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
                        'replacement_source_card_config_name': '付替元カード設定名',
                        'replacement_source_card_number': '付替元カード番号',
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
class OpenApiTransactionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Success',
            summary='Success',
            value=[{
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
            }],
            response_only=True,
            status_codes=['200']
        )
    ]
)
class OpenApiTransactionListCsvSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Success',
            summary='Success',
            value=[{
                'card_config_name': 'カード設定名',
                'company_name': '企業名',
                'shop_name': '店舗名',
                'terminal_number': '端末番号',
                'management_tag_name': '管理タグ名',
                'sumamry': [{
                    'summary_day': '集計年月日',
                    'summary_month': '集計年月',
                    'summary_year': '集計年',
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
                        'value_total_count': '前払バリュー合計件数',
                        'value_cancel_total_amount': '前払バリュー取消合計額',
                        'value_cancel_total_count': '前払バリュー取消合計件数',
                        'payable_bonus_total_amount': '決済併用ボーナス合計額',
                        'payable_bonus_total_count': '決済併用ボーナス合計件数',
                        'payable_bonus_cancel_total_amount': '決済併用ボーナス取消合計額',
                        'payable_bonus_cancel_total_count': '決済併用ボーナス取消合計件数',
                    },
                    'grant': {
                        'value_total_amount': '前払バリュー付与合計額',
                        'value_total_count': '前払バリュー付与合計件数',
                        'value_cancel_total_amount': '前払バリュー付与取消合計額',
                        'value_cancel_total_count': '前払バリュー付与取消合計件数',
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
                    },
                    'balance': {
                        'enable': {
                            'value_total_amount': '前払いバリュー有効残高',
                            'payable_bonus_amount': '決済併用ボーナス有効残高',
                            'exchange_bonus_amount': '商品交換ボーナス有効残高',
                        },
                        'disable': {
                            'value_total_amount': '前払いバリュー無効残高',
                            'payable_bonus_amount': '決済併用ボーナス無効残高',
                            'exchange_bonus_amount': '商品交換ボーナス無効残高',
                        }
                    }
                }]
            }],
            response_only=True,
            status_codes=['200']
        )
    ]
)
class OpenApiCardTransactionSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Success',
            summary='Success',
            value=[{
                'card_config_name': 'カード設定名',
                'sumamry': [{
                    'summary_month': '集計年月',
                    'summary_year': '集計年',
                    'charge': {
                        'charge_total_amount': 'チャージ合計額',
                        'charge_cancel_total_amount': 'チャージ取消合計額'
                    },
                    'payment': {
                        'value_total_amount': '前払バリュー合計額',
                        'value_cancel_total_amount': '前払バリュー取消合計額'
                    },
                    'grant': {
                        'value_total_amount': '前払バリュー付与合計額',
                        'value_cancel_total_amount': '前払バリュー付与取消合計額'
                    },
                    'balance': {
                        'enable': {
                            'value_total_amount': '前払いバリュー有効残高'
                        },
                        'disable': {
                            'value_total_amount': '前払いバリュー無効残高'
                        }
                    }
                }]
            }],
            response_only=True,
            status_codes=['200']
        )
    ]
)
class OpenApiBalanceSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Success',
            summary='Success',
            value=[{
                'event_name': 'イベント名',
                'company_name': '企業名',
                'shop_name': '店舗名',
                'management_tag_name': '管理タグ名',
                'sumamry': [{
                    'summary_day': '集計年月日',
                    'summary_month': '集計年月',
                    'summary_year': '集計年',
                    'payment': {
                        'total_amount': '決済合計額',
                        'cancel_total_amount': '決済取消合計額',
                        'value_total_amount': '前払バリュー合計額',
                        'value_cancel_total_amount': '前払バリュー取消合計額',
                        'payable_bonus_total_amount': '決済併用ボーナス合計額',
                        'payable_bonus_cancel_total_amount': '決済併用ボーナス取消合計額',
                    },
                    'grant': {
                        'value_total_amount': '前払バリュー付与合計額',
                        'value_cancel_total_amount': '前払バリュー付与取消合計額',
                        'payable_bonus_total_amount': '決済併用ボーナス付与合計額',
                        'payable_bonus_cancel_total_amount': '決済併用ボーナス付与取消合計額',
                        'exchange_bonus_total_amount': '商品交換ボーナス付与合計額',
                        'exchange_bonus_cancel_total_amount': '商品交換ボーナス付与取消合計額',
                    },
                    'used': {
                        'exchange_bonus_total_amount': '商品交換ボーナス合計額利用',
                        'exchange_bonus_cancel_total_amount': '商品交換ボーナス取消合計額利用',
                    },
                    'balance': {
                        'enable': {
                            'value_total_amount': '前払いバリュー有効残高(強制付与のみ)',
                            'payable_bonus_amount': '決済併用ボーナス有効残高',
                            'exchange_bonus_amount': '商品交換ボーナス有効残高',
                        },
                        'disable': {
                            'value_total_amount': '前払いバリュー無効残高(強制付与のみ)',
                            'payable_bonus_amount': '決済併用ボーナス無効残高',
                            'exchange_bonus_amount': '商品交換ボーナス無効残高',
                        }
                    }
                }]
            }],
            response_only=True,
            status_codes=['200']
        )
    ]
)
class OpenApiEventSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"

    def create(self, validated_data):
        transaction = Transaction(
        )
        transaction.save()
        return transaction


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Success',
            summary='Success',
            value=[{
                'card_config_name': 'カード設定名',
                'sumamry': [{
                    'summary_day': '集計年月日',
                    'card_status': {
                        'not_activate': 0,
                        'activated': 0,
                        'stoped': 0,
                        'replaced': 0,
                        'destroyed': 0
                    }
                }]
            }],
            response_only=True,
            status_codes=['200']
        )
    ]
)
class OpenApiCardIssueTotalSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"

    def create(self, validated_data):
        transaction = Transaction(
        )
        transaction.save()
        return transaction


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Success',
            summary='Success',
            value={
                'sumamry': [{
                    'summary_day': '集計年月日',
                    'card_status': {
                        'not_activate': 0,
                        'activated': 0,
                        'stoped': 0,
                        'replaced': 0,
                        'destroyed': 0
                    }
                }]
            },
            response_only=True,
            status_codes=['200']
        )
    ]
)
class OpenApiCardIssueTransitionSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Success',
            summary='Success',
            value={
                'request_id': '申請ID'
            },
            response_only=True,
            status_codes=['200']
        )
    ]
)
class OpenApiTransactionCancelRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Success',
            summary='Success',
            value={
                'request_id': '申請ID',
                'request_user_mail_address': '申請者メールアドレス',
                'request_user_name': '申請者名',
                'request_type': '申請種別',
                'request_status': 1,
                'requested_at': '申請日時',
                'transaction': {
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
                            'replacement_source_card_config_name': '付替元カード設定名',
                            'replacement_source_card_number': '付替元カード番号',
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
                }
            },
            response_only=True,
            status_codes=['200']
        )
    ]
)
class OpenApiTransactionCancelRequestDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Success',
            summary='Success',
            value=[{
                'requests': {
                    'request_id': '申請ID',
                    'request_user_mail_address': '申請者メールアドレス',
                    'request_user_name': '申請者名',
                    'request_type': '申請種別',
                    'request_status': 1,
                    'requested_at': '申請日時',
                }
            }],
            response_only=True,
            status_codes=['200']
        )
    ]
)
class OpenApiRequestListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"


class ManagementTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagementTag
        fields = ['name', ]

    def to_representation(self, obj):
        return obj.name
