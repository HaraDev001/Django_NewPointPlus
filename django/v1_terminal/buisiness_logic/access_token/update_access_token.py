from rest_framework import status

from v1_terminal.buisiness_logic.DTO.access_token_issue_response \
    import TerminalAccessTokenIssueResponse
from v1_terminal.data.ITerminalAccessTokenRepository \
    import ITerminalAccessTokenRepository

from .common import create_access_token, decode_token_to_json

from utils.datetime_utility import (now,
                                    to_utc_timestamp
                                    )


class UpdateAccessToken:
    '''アクセストークンを更新するクラス

        アクセストークンを更新する

        Attributes:
            repository (ITerminalAccessTokenRepository型):
                        ITerminalAccessTokenRepositoryを継承したオブジェクト
    '''

    def __init__(self, repository: ITerminalAccessTokenRepository):
        self.repository: ITerminalAccessTokenRepository = repository

    def execute(self, refresh_token):
        '''アクセストークンを更新する.

        1) メールアドレス、パスワード、店舗端末番号から店舗端末情報を取得する.
        2) 事業者利用規約に同意済みをチェックする.
        3) 店舗端末が有効となっているかをチェックする.

        1), 2), 3) すべて満たされれば、アクセストークンを更新し、「有効」な認証情報として保存する.

        それ以外はアクセストークンを発行しない.

        Args:
            refresh_token (str型): リフレッシュトークン.

        Returns:
            TerminalAccessTokenIssueResponse型:
                   アクセストークン, アクセストークン有効期限, リフレッシュトークンを含む.
            int型: HTTPステータスコード

        '''

        # refresh_tokenをデコードし、メールアドレス、店舗端末番号を取得する。
        token_payload_json = decode_token_to_json(refresh_token)

        mail_address = token_payload_json['mail_address']
        terminal_no = token_payload_json['terminal_no']

        # 店舗端末情報を取得する。
        try:
            terminal = self.repository.get_terminal(terminal_no)
            if terminal.company_user_policy is False:
                # 事業者利用規約に未同意
                # 現状、200しか定義されていない
                return None, status.HTTP_200_OK
        except Exception:
            # 店舗端末番号で一致する店舗端末情報がない
            # 現状、200しか定義されていない
            return None, status.HTTP_200_OK

        try:
            # メールアドレス、店舗端末番号から店舗端末認証情報を取得する。
            target_token_info = self.repository.get_terminal_access_authorization(
                mail_address, terminal_no
            )
        except Exception:
            # 店舗端末認証情報が取得できなかった。
            # 現状、200しか定義されていない
            return None, status.HTTP_200_OK

        if target_token_info.state == 1:
            # アクセストークンは有効
            current_unixtime = int(to_utc_timestamp(now()))
            if current_unixtime <= target_token_info.access_token_expire_at:
                # アクセストークンは有効期限内

                # 新しいアクセストークンを発行する。
                token = create_access_token(mail_address, terminal_no)

                # アクセストークンの状態：1 (有効)
                # 仮の状態。モデルが定義されたら書き換える。
                access_token_state = 1

                # 店舗端末認証情報を保存
                target_token_info.mail_address = mail_address
                target_token_info.terminal_no = terminal_no
                target_token_info.access_token = token[0]
                target_token_info.access_token_expire_at = token[1]
                target_token_info.refresh_token = token[2]
                target_token_info.refresh_token_expire_at = token[3]
                target_token_info.state = access_token_state

                self.repository.save_terminal_access_authorization(target_token_info)

                return (
                    TerminalAccessTokenIssueResponse(
                        access_token=token[0],
                        access_token_expire_at=token[1],
                        refresh_token=token[2]
                        ), status.HTTP_200_OK
                    )
        # アクセストークンは、発行前(0) か 無効(9) か 有効(1) のいずれか
        # 無効とする。
        # 仮の状態。モデルが定義されたら書き換える。
        access_token_state = 9

        # 店舗端末認証情報を保存
        target_token_info.state = access_token_state

        self.repository.save_terminal_access_authorization(target_token_info)

        return None, status.HTTP_200_OK
