
from v1_terminal.data.ITerminalAccessTokenRepository import ITerminalAccessTokenRepository

from .common import decode_token_to_json

from utils.datetime_utility import (now,
                                    to_utc_timestamp
                                    )

import uuid


class EvaluateAccessToken:
    '''アクセストークンを評価するクラス

        アクセストークンを評価する

        Attributes:
            repository (ITerminalAccessTokenRepository型):
                    ITerminalAccessTokenRepositoryを継承したオブジェクト
    '''

    def __init__(self, repository: ITerminalAccessTokenRepository):
        self.repository: ITerminalAccessTokenRepository = repository

    def execute(self, access_token):

        # access_tokenをデコードしメールアドレス、店舗端末番号を取得する。
        access_token_payload_json = decode_token_to_json(access_token)

        mail_address = access_token_payload_json['mail_address']
        terminal_no = access_token_payload_json['terminal_no']

        try:
            # メールアドレス、店舗端末番号から店舗端末認証情報を取得する。
            target_token_info = self.repository.get_terminal_access_authorization(
                mail_address, terminal_no
            )
        except Exception:
            # 店舗端末認証情報が取得できなかった。
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
