from django.test import SimpleTestCase
from datetime import timedelta
from freezegun import freeze_time
from utils import signer_utility


class TestSignerUtiliy(SimpleTestCase):
    '''暗号署名テスト'''

    UNAVAILABLE_TOKEN = 'eyJhY2NvdW50aW5nX2lkIjoiYjUxNzlhMzAtM2M5ZS00ZDFkLTlkZjktYWJlMWIyYmU4OTYyIn0:1lbHnn:sf-WTKQs_xRB_db8StfJndARu2AZqR3LLWvgo9BzKtZ'
    data = {
        'test_id': 'b5179a30-3c9e-4d1d-9df9-abe1b2be8962'
    }

    def test_singed_unsigned(self):
        '''正常：暗号署名 → 複合化'''

        token = signer_utility.sign(self.data)
        unsign_status, unsign_code = signer_utility.unsign(token)
        self.assertEqual(signer_utility.SignerUtilityStatus.UNSIGN_FINISH, unsign_status)
        self.assertEqual(self.data, unsign_code)

        with freeze_time(timedelta(days=365*50)):
            unsign_status, unsign_code = signer_utility.unsign(token)
            self.assertEqual(signer_utility.SignerUtilityStatus.UNSIGN_FINISH, unsign_status)
            self.assertEqual(self.data, unsign_code)

    def test_singed_timestamp_unsigned_10minutes(self):
        '''正常：暗号署名（タイムスタンプあり） → 10分後複合化'''

        token = signer_utility.sign_timestamp(self.data)

        # 10分進んだ体でテスト。DEFAULT_EXPIRATION_TIME_AT_SECOND値で判定
        with freeze_time(timedelta(minutes=10)):
            unsign_status, unsign_code = signer_utility.unsign_expiration_check(token)
            self.assertEqual(signer_utility.SignerUtilityStatus.UNSIGN_FINISH, unsign_status)
            self.assertEqual(self.data, unsign_code)

    def test_singed_timestamp_unsigned_time_out(self):
        ''' 期限切れテスト：暗号署名（タイムスタンプあり） → 複合 → タイムアウト'''

        token = signer_utility.sign_timestamp(self.data)

        # 1時間進んだ体でテスト
        with freeze_time(timedelta(hours=1)):
            # DEFAULT_EXPIRATION_TIME_AT_SECOND値で判定
            unsign_status, unsign_code = signer_utility.unsign_expiration_check(token)
            self.assertEqual(signer_utility.SignerUtilityStatus.UNSIGN_EXPIRED, unsign_status)

            # 有効期限5分以内としてで判定
            unsign_status, unsign_code = signer_utility.unsign_expiration_check(token, 60*5)
            self.assertEqual(signer_utility.SignerUtilityStatus.UNSIGN_EXPIRED, unsign_status)

    def test_singed_unsigned_(self):
        ''' 無効トークンテスト：暗号署名 → 複合 → 無効なトークン'''

        unsign_status, unsign_code = signer_utility.unsign_expiration_check(self.UNAVAILABLE_TOKEN, 5)
        self.assertEqual(signer_utility.SignerUtilityStatus.UNSIGN_BAD_SIGNATURE, unsign_status)

        unsign_status, unsign_code = signer_utility.unsign(self.UNAVAILABLE_TOKEN)
        self.assertEqual(signer_utility.SignerUtilityStatus.UNSIGN_BAD_SIGNATURE, unsign_status)

    def test_singed_unsigned_expiration_check(self):
        ''' 暗号化、復号化時に関数違い複合エラー '''

        # 暗号化(タイムスタンプなし)
        token = signer_utility.sign(self.data)
        # 復号化→タイムスタンプがないので無効なトークン扱い
        unsign_status, unsign_code = signer_utility.unsign_expiration_check(token, 5)
        self.assertEqual(signer_utility.SignerUtilityStatus.UNSIGN_BAD_SIGNATURE, unsign_status)

        # 暗号化(タイムスタンプあり)
        token = signer_utility.sign_timestamp(self.data)
        # 復号化→タイムスタンプ用ではないので失敗
        unsign_status, unsign_code = signer_utility.unsign(token)
        self.assertEqual(signer_utility.SignerUtilityStatus.UNSIGN_BAD_SIGNATURE, unsign_status)
