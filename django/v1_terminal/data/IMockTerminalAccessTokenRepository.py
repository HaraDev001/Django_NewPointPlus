from v1_terminal.data.ITerminalAccessTokenRepository \
    import ITerminalAccessTokenRepository

from unittest import mock


class IMockTerminalAccessTokenRepository(
    ITerminalAccessTokenRepository
):
    '''店舗端末を発行/更新/失効/評価するためにモデルのモックを操作するクラス

        Attributes:
            terminals (dict型): 店舗端末情報を保持する.
            tertminal_access_authorization (dict型): 店舗端末認証情報を保持する.
    '''
    def __init__(self):

        # 店舗端末を操作するユーザー
        user_01_T = mock.MagicMock(
            mail_address='terminal.01@example.co.jp', password='terminal.01.password',
            authority_to_use_terminal=True
        )
        user_02_F = mock.MagicMock(
            mail_address='terminal.02@example.co.jp', password='terminal.02.password',
            authority_to_use_terminal=False
        )

        # 店舗端末情報
        self.terminals = dict()
        terminal_01_T_1 = mock.MagicMock(
            terminal_no='terminal_01',
            company_user_policy=True, state=1,
            users=[user_01_T, user_02_F]
            )
        terminal_02_T_2 = mock.MagicMock(
            terminal_no='terminal_02',
            company_user_policy=True, state=2,
            users=[user_01_T, user_02_F]
            )
        terminal_03_F_1 = mock.MagicMock(
            terminal_no='terminal_03',
            company_user_policy=False, state=1,
            users=[user_01_T, user_02_F]
            )
        terminal_04_F_2 = mock.MagicMock(
            terminal_no='terminal_04',
            company_user_policy=False, state=2,
            users=[user_01_T, user_02_F]
            )

        for terminal in [
                    terminal_01_T_1, terminal_02_T_2,
                    terminal_03_F_1, terminal_04_F_2
                ]:
            key = terminal.terminal_no
            self.terminals[key] = terminal

        # 店舗端末認証情報
        self.tertminal_access_authorization = dict()

    def identify(self, mail_address, password, terminal_no):
        '''店舗端末を認証し、店舗端末情報を取得する.

            メールアドレス、パスワード、店舗端末番号に一致する店舗端末情報を取得する

        Args:
            mail_address (str型): メールアドレス.
            password (str型): パスワード
            terminal_no (str型): 店舗端末番号.

        Returns:
            店舗端末情報: 指定されたメールアドレス、パスワードおよび店舗端末番号に
                        　一致するモックオブジェクトがなければ、例外を発生させる.

        Raises:
            Exception: リクエストされたメールアドレス、パスワードで一致する店舗端末情報がない
            Exception: リクエストされた店舗端末番号で一致する店舗端末情報がない

        '''
        key = terminal_no
        try:
            terminal = self.terminals[key]
            for user in terminal.users:
                if user.mail_address == mail_address and user.password == password:
                    return terminal
            raise Exception(
                'リクエストされたメールアドレス、パスワードで一致する店舗端末情報がない'
            )
        except KeyError:
            raise Exception(
                'リクエストされた店舗端末番号で一致する店舗端末情報がない'
                )

    def get_terminal(self, terminal_no):
        '''店舗端末情報を取得する.

            店舗端末番号に一致する店舗端末情報を取得する

        Args:
            terminal_no (str型): 店舗端末番号.

        Returns:
            店舗端末情報: 指定された店舗端末番号に一致するモックオブジェクトがなければ、例外を発生させる.

        Raises:
            Exception: リクエストされた店舗端末番号で一致する店舗端末情報がない

        '''
        key = terminal_no
        try:
            terminal = self.terminals[key]
            return terminal
        except KeyError:
            raise Exception(
                'リクエストされた店舗端末番号で一致する店舗端末情報がない'
                )

    def get_terminal_access_authorization(self, mail_address, terminal_no):
        '''店舗端末認証情報を取得する.

            店舗端末認証情報を取得する.

        Args:
            mail_address (str型): メールアドレス.
            terminal_no (str型): 店舗端末番号.

        Returns:
            店舗端末認証情報: 指定されたメールアドレスおよび店舗端末番号に
                              一致するモックオブジェクトがなければ、例外を発生させる.

        Raises:
            Exception: リクエストされたメールアドレスおよび店舗端末番号で一致する店舗端末認証情報がない

        '''
        try:
            key = mail_address + terminal_no
            return self.tertminal_access_authorization[key]
        except KeyError:
            raise Exception(
                'リクエストされたメールアドレスおよび店舗端末番号で一致する店舗端末認証情報がない'
                )
        except Exception as e:
            raise e

    def get_or_create_terminal_access_authorization(self, mail_address, terminal_no):
        '''店舗端末認証情報を取得する.

            店舗端末認証情報を取得する.

        Args:
            mail_address (str型): メールアドレス.
            terminal_no (str型): 店舗端末番号.

        Returns:
            店舗端末認証情報: 指定されたメールアドレスおよび店舗端末番号に
                              一致するモックオブジェクトがなければ、新しいモックオブジェクトを作成する.

        Raises:
            Exception: リクエストされたメールアドレスおよび店舗端末番号で一致する店舗端末情報がない

        '''
        try:
            key = mail_address + terminal_no
            return self.tertminal_access_authorization[key]
        except KeyError:
            return mock.MagicMock()

    def save_terminal_access_authorization(self, terminal_access_auth):
        '''店舗端末認証情報を保存する.

           店舗端末認証情報を保存する.

        Args:
            terminal_access_auth (MagicMock型): モックオブジェクト.

        Returns:
            なし

        '''
        key = terminal_access_auth.mail_address + terminal_access_auth.terminal_no
        self.tertminal_access_authorization[key] = terminal_access_auth

    def is_user_having_authority_to_user_terminal(self, mail_address, terminal) -> bool:
        '''ユーザーが店舗端末を操作する権限を持っているかをチェックする.

           ユーザーが店舗端末を操作する権限を持っているかをチェックする.

        Args:
            mail_address (str型): メールアドレス.
            terminal (MagicMock型): 店舗端末情報.

        Returns:
            True: ユーザーは指定の店舗端末を操作する権限を持っている.
            False: ユーザーは指定の店舗端末を操作する権限を持っていない.
        '''
        for user in terminal.users:
            if mail_address == user.mail_address:
                if user.authority_to_use_terminal:
                    return True
        return False
