from rest_framework import status
from django.test import SimpleTestCase
from v1_card.data.IAccessTokenRepository import IAccessTokenRepository
from v1_card.data.IMockAccessTokenRepository import IMockAccessTokenRepository
from v1_card.buisiness_logic.access_token.issue_access_token \
    import IssueAccessToken
from v1_card.buisiness_logic.access_token.evaluate_access_token \
    import EvaluateAccessToken

from v1_card.buisiness_logic.access_token.common import decode_token_to_json

from utils.datetime_utility import (now,
                                    to_utc_timestamp,
                                    get_datetime_hours_later_from
                                    )


class AccessTokenEvaluateTests(SimpleTestCase):

    # カード情報[あり] アクティベート [済み] 決済 [可能] サービス利用許可 [あり] 事業者利用規約 [同意]
    def test_send_card_101_success(self):
        # 予めアクセストークンを発行しておく
        test_repository: IAccessTokenRepository = IMockAccessTokenRepository()
        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute('9999999999990101', '0101')

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNotNone(access_token_response)

        access_token_payload_json = decode_token_to_json(
            access_token_response.access_token)

        self.assertEqual(
            access_token_payload_json['card_no'], '9999999999990101'
            )

        card_access_auth = test_repository.get_card_access_authorization('9999999999990101')
        # 有効となっているか
        self.assertEqual(card_access_auth.state, 1)

        utc_timestamp_current = to_utc_timestamp(
            now()
        )

        utc_timestamp_1_hour_later = to_utc_timestamp(
            get_datetime_hours_later_from(now(), hours=1)
        )

        # アクセストークンの有効期限
        self.assertLessEqual(
            utc_timestamp_current,
            access_token_response.access_token_expire_at
            )

        self.assertLessEqual(
            access_token_response.access_token_expire_at,
            utc_timestamp_1_hour_later
            )

        # 評価
        evalueate_access_token = EvaluateAccessToken(test_repository)
        principal_id = evalueate_access_token.execute(
                access_token_response.access_token
                )

        # principal ID はNoneではない
        self.assertIsNotNone(principal_id)

    def test_send_card_101_expired_fail(self):
        # 予めアクセストークンを発行しておく
        test_repository: IAccessTokenRepository = IMockAccessTokenRepository()
        issue_access_token = IssueAccessToken(test_repository)

        access_token_response, status_code = \
            issue_access_token.execute('9999999999990101', '0101')

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertIsNotNone(access_token_response)

        access_token_payload_json = decode_token_to_json(
            access_token_response.access_token)

        self.assertEqual(
            access_token_payload_json['card_no'], '9999999999990101'
            )

        card_access_auth = test_repository.get_card_access_authorization('9999999999990101')
        # 有効となっているか
        self.assertEqual(card_access_auth.state, 1)

        # 有効期限切れにする。
        card_access_auth.access_token_expire_at = 0

        # 評価
        evalueate_access_token = EvaluateAccessToken(test_repository)
        principal_id = evalueate_access_token.execute(
                access_token_response.access_token
                )

        # principal ID はNoneである。
        self.assertIsNone(principal_id)
