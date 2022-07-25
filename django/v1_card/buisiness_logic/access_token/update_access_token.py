from rest_framework import status

from v1_card.buisiness_logic.DTO.access_token_issue_response import AccessTokenIssueResponse
from v1_card.data.IAccessTokenRepository import IAccessTokenRepository

from .common import create_access_token, decode_token_to_json

from utils.datetime_utility import (now,
                                    to_utc_timestamp
                                    )


class UpdateAccessToken:
    '''アクセストークンを更新するクラス

        アクセストークンを更新する

        Attributes:
            repository (IAccessTokenRepository型): IAccessTokenRepositoryを継承したオブジェクト
    '''

    def __init__(self, repository: IAccessTokenRepository):
        self.repository: IAccessTokenRepository = repository

    def execute(self, refresh_token):
        '''アクセストークンを更新する.

        1) リフレッシュトークンからカード情報を取得する.
        2) サービス利用許可あり、事業者利用規約に同意済み、を確認する.
        3) カードアクセス認証情報を取得する.
        4) カードアクセス認証情報が有効かつ有効期限内であることを確認する.
        5) 4)を満たす場合、新しいアクセストークンを発行し、有効アクセストークンとして
           カードアクセス認証情報を保存する.
        6) 4)を満たさない場合、アクセストークン未発行として、カードアクセス認証情報を保存する.

        Args:
            refresh_token (str型): リフレッシュトークン.

        Returns:
            AccessTokenIssueResponse型: アクセストークン, アクセストークン有効期限, リフレッシュトークンを含む.
            int型: HTTPステータスコード

        '''

        # refresh_tokenをデコードし、カード番号を取得する。
        token_payload_json = decode_token_to_json(refresh_token)

        card_no = token_payload_json['card_no']

        # カード情報を取得
        try:
            card = self.repository.get_card(card_no)
        except Exception:
            # カード番号に一致するカードがない
            return None, status.HTTP_401_UNAUTHORIZED

        if (card.service_user_policy is False or card.company_user_policy is False):
            # サービス利用許可なし、事業者利用規約に未同意
            return None, status.HTTP_403_FORBIDDEN

        try:
            # カード番号からカード認証情報を取得する。
            target_token_info = self.repository.get_card_access_authorization(card_no)
        except Exception:
            # カード認証情報が取得できなかった。
            return None, status.HTTP_401_UNAUTHORIZED

        if target_token_info.state == 1:
            # アクセストークンは有効
            current_unixtime = int(to_utc_timestamp(now()))
            if current_unixtime <= target_token_info.access_token_expire_at:
                # アクセストークンは有効期限内

                # 新しいアクセストークンを発行する。
                token = create_access_token(card_no)

                # アクセストークンの状態：1 (有効)
                # 仮の状態。モデルが定義されたら書き換える。
                access_token_state = 1

                # カードアクセス認証情報を保存
                target_token_info.card_no = card_no
                target_token_info.access_token = token[0]
                target_token_info.access_token_expire_at = token[1]
                target_token_info.refresh_token = token[2]
                target_token_info.refresh_token_expire_at = token[3]
                target_token_info.state = access_token_state

                self.repository.save_card_access_authorization(target_token_info)

                return (
                    AccessTokenIssueResponse(
                        access_token=token[0],
                        access_token_expire_at=token[1],
                        refresh_token=token[2]
                        ), status.HTTP_200_OK
                    )
        # アクセストークンは、発行前(0) か 無効(9) か 有効(1)でも有効期限が切れている のいずれか
        # 無効とする。
        # アクセストークンの状態：1 (有効)
        # 仮の状態。モデルが定義されたら書き換える。
        access_token_state = 9

        # カードアクセス認証情報を保存
        target_token_info.state = access_token_state

        self.repository.save_card_access_authorization(target_token_info)

        return None, status.HTTP_200_OK
