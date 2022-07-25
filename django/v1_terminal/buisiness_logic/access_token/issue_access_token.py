from rest_framework import status

from v1_terminal.data.ITerminalAccessTokenRepository import ITerminalAccessTokenRepository
from v1_terminal.buisiness_logic.DTO.access_token_issue_response import TerminalAccessTokenIssueResponse

from .common import create_access_token


class IssueAccessToken:
    '''アクセストークンを発行するクラス

        アクセストークンを発行する

        Attributes:
            repository (ITerminalAccessTokenRepository型):
                        ITerminalAccessTokenRepositoryを継承したオブジェクト
    '''

    def __init__(self, repository: ITerminalAccessTokenRepository):
        self.repository: ITerminalAccessTokenRepository = repository

    def execute(self, mail_address, password, terminal_no):
        '''アクセストークンを発行する.

        1) メールアドレス、パスワード、店舗端末番号から店舗端末情報を取得する.
        2) 事業者利用規約に同意済みをチェックする.
        3) 店舗端末が有効となっているかをチェックする.
        4) メールアドレス、パスワードで認証されたユーザーが、店舗端末を操作する権限を
           持っているかをチェックする.

        1), 2), 3), 4) すべて満たされれば、アクセストークンを発行し、「有効」な認証情報として保存する.

        それ以外はアクセストークンを発行しない.

        Args:
            mail_address (str型): メールアドレス.
            password (str型): パスワード.
            terminal_no (str型): 店舗端末番号.
        Returns:
            TerminalAccessTokenIssueResponse型:
                   アクセストークン, アクセストークン有効期限, リフレッシュトークンを含む.
            int型: HTTPステータスコード

        '''

        # 店舗端末情報を取得
        try:
            terminal = self.repository.identify(mail_address, password, terminal_no)
        except Exception:
            # リクエストされたメールアドレス、パスワード、店舗端末番号で一致する店舗端末情報がない
            # リクエストされたメールアドレスおよび店舗端末番号で一致する店舗端末情報がない
            # 現状、200しか定義されていない
            return None, status.HTTP_200_OK

        if terminal.company_user_policy is False:
            # 事業者利用規約に未同意
            # 現状、200しか定義されていない
            return None, status.HTTP_200_OK

        # 店舗端末は有効であるかチェック
        # state == 1 で有効は、仮の状態。モデルが定義されたら書き換える。
        if terminal.state == 1:
            # 店舗端末は有効である

            if self.repository.is_user_having_authority_to_user_terminal(
                mail_address, terminal
            ):

                # ユーザーは指定の店舗端末を操作する権限を持っている

                # アクセストークンを生成する
                token = create_access_token(mail_address, terminal_no)

                # アクセストークンの状態：1 (有効)
                # 仮の状態。モデルが定義されたら書き換える。
                access_token_state = 1

                # 店舗認証情報を保存
                terminal_access_auth = \
                    self.repository.get_or_create_terminal_access_authorization(
                        mail_address, terminal_no)

                terminal_access_auth.mail_address = mail_address
                terminal_access_auth.terminal_no = terminal_no
                terminal_access_auth.access_token = token[0]
                terminal_access_auth.access_token_expire_at = token[1]
                terminal_access_auth.refresh_token = token[2]
                terminal_access_auth.refresh_token_expire_at = token[3]
                terminal_access_auth.state = access_token_state

                self.repository.save_terminal_access_authorization(terminal_access_auth)

                return (
                    TerminalAccessTokenIssueResponse(
                        access_token=token[0],
                        access_token_expire_at=token[1],
                        refresh_token=token[2]
                        ), status.HTTP_200_OK
                    )

        # アクセストークンの状態：0 (未発行)
        # 仮の状態。モデルが定義されたら書き換える。
        access_token_state = 0

        # 店舗認証情報を保存
        terminal_access_auth = \
            self.repository.get_or_create_terminal_access_authorization(mail_address, terminal_no)

        terminal_access_auth.mail_address = mail_address
        terminal_access_auth.terminal_no = terminal_no
        terminal_access_auth.access_token = None
        terminal_access_auth.access_token_expire_at = -1
        terminal_access_auth.refresh_token = None
        terminal_access_auth.refresh_token_expire_at = -1
        terminal_access_auth.state = access_token_state

        self.repository.save_terminal_access_authorization(terminal_access_auth)

        return None, status.HTTP_200_OK
