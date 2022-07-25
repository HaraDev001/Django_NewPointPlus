from rest_framework import status

from v1_terminal.data.ITerminalAccessTokenRepository import ITerminalAccessTokenRepository

from .common import decode_token_to_json


class InvalidateAccessToken:
    '''アクセストークンを無効にするクラス

        アクセストークンを無効にする

        Attributes:
            repository (ITerminalAccessTokenRepository型):
                    ITerminalAccessTokenRepositoryを継承したオブジェクト
    '''

    def __init__(self, repository: ITerminalAccessTokenRepository):
        self.repository: ITerminalAccessTokenRepository = repository

    def execute(self, access_token, refresh_token):

        # アクセストークン、リフレッシュトークンをDBに保存するモデルであれば、
        # 両方を無効にする必要がある。
        # モデルが定義されるまでは、店舗端末認証情報にトークンを格納しない想定で
        # アクセストークンのみを使用して無効にする処理にしておく。

        # access_tokenをデコードしメールアドレス、店舗端末番号を取得する。
        access_token_payload_json = decode_token_to_json(access_token)
        # refresh_token_payload_json = decode_token_to_json(refresh_token)

        mail_address = access_token_payload_json['mail_address']
        terminal_no = access_token_payload_json['terminal_no']

        try:
            # メールアドレス、店舗端末番号から店舗端末認証情報を取得する。
            target_token_info = self.repository.get_terminal_access_authorization(
                mail_address, terminal_no
            )
        except Exception:
            # 店舗端末認証情報が取得できなかった。
            # 現状、200しか定義されていない
            return status.HTTP_200_OK

        # アクセストークンは、発行前(0) か 無効(9) か 有効(1) のいずれか
        # 無効とする。
        # 仮の状態。モデルが定義されたら書き換える。
        access_token_state = 9

        # 店舗端末認証情報を保存
        target_token_info.state = access_token_state

        self.repository.save_terminal_access_authorization(target_token_info)

        return status.HTTP_200_OK
