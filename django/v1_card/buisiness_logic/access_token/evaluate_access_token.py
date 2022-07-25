from v1_card.data.IAccessTokenRepository import IAccessTokenRepository

from .common import decode_token_to_json

from utils.datetime_utility import (now,
                                    to_utc_timestamp
                                    )

import uuid


class EvaluateAccessToken:
    '''アクセストークンを評価するクラス

        アクセストークンを評価する

        Attributes:
            repository (IAccessTokenRepository型): IAccessTokenRepositoryを継承したオブジェクト
    '''

    def __init__(self, repository: IAccessTokenRepository):
        self.repository: IAccessTokenRepository = repository

    def execute(self, access_token):
        '''アクセストークンを評価する.

        1) アクセストークンからカードアクセス認証情報を取得する.
        2) アクセストークンを無効として、カードアクセス認証情報を保存する。
        3) カードアクセス認証情報が有効かつ有効期限内であることを確認する.
        4) 3)を満たす場合、Principal IDとしてUUIDを発行する.
        5) 4)を満たさない場合、Principal IDを発行しない.

        3)を満たさない場合、Principal IDを発行しない.

        Args:
            access_token (str型): アクセストークン.

        Returns:
            str型: UUID型をstr型にして返す.

        '''

        # access_tokenをデコードし、カード番号を取得する。
        access_token_payload_json = decode_token_to_json(access_token)
        # refresh_token_payload_json = decode_token_to_json(refresh_token)

        card_no = access_token_payload_json['card_no']

        try:
            # カード番号からカード認証情報を取得する。
            target_token_info = self.repository.get_card_access_authorization(card_no)
        except Exception:
            # カード認証情報が取得できなかった。
            # UUIDの発行はない。
            return None

        if target_token_info.state == 1:
            # アクセストークンは有効
            current_unixtime = int(to_utc_timestamp(now()))
            if current_unixtime <= target_token_info.access_token_expire_at:
                # アクセストークンは有効期限内

                # UUIDを発行し、principal IDとする。
                return str(uuid.uuid4())

        # UUIDの発行はない。
        return None
