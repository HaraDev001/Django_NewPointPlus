from rest_framework import status

from v1_card.data.IAccessTokenRepository import IAccessTokenRepository

from .common import decode_token_to_json


class InvalidateAccessToken:
    '''アクセストークンを無効にするクラス

        アクセストークンを無効にする

        Attributes:
            repository (IAccessTokenRepository型): IAccessTokenRepositoryを継承したオブジェクト
    '''

    def __init__(self, repository: IAccessTokenRepository):
        self.repository: IAccessTokenRepository = repository

    def execute(self, access_token, refresh_token):
        '''アクセストークンを失効する.

        1) アクセストークンからカード情報を取得する.
        2) カードアクセス認証情報を取得する.
        3) アクセストークンを無効として、カードアクセス認証情報を保存する。

        Args:
            access_token (str型): アクセストークン.
            refresh_token (str型): リフレッシュトークン.

        Returns:
            int型: HTTPステータスコード

        '''

        # アクセストークン、リフレッシュトークンをDBに保存するモデルであれば、
        # 両方を無効にする必要がある。
        # モデルが定義されるまでは、カードアクセス認証情報にトークンを格納しない想定で
        # アクセストークンのみを使用して無効にする処理にしておく。

        # access_tokenをデコードし、カード番号を取得する。
        access_token_payload_json = decode_token_to_json(access_token)
        # refresh_token_payload_json = decode_token_to_json(refresh_token)

        card_no = access_token_payload_json['card_no']

        try:
            # カード番号からカード認証情報を取得する。
            target_token_info = self.repository.get_card_access_authorization(card_no)
        except Exception:
            # カード認証情報が取得できなかった。
            return status.HTTP_401_UNAUTHORIZED

        # アクセストークンは、発行前(0) か 無効(9) か 有効(1) のいずれか
        # 無効とする。
        # アクセストークンの状態：1 (有効)
        # 仮の状態。モデルが定義されたら書き換える。
        access_token_state = 9

        # カードアクセス認証情報を保存
        target_token_info.state = access_token_state

        self.repository.save_card_access_authorization(target_token_info)

        return status.HTTP_200_OK
