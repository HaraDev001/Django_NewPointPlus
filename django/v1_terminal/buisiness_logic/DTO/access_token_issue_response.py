class TerminalAccessTokenIssueResponse:
    '''TerminalAccessTokenIssueResponseクラス

        アクセストークン発行するIssueAccessTokenからSerializerへ渡されるDTOクラス

        Attributes:
            access_token (str型): アクセストークン.
            access_token_expire_at (int型): アクセストークン有効期限. 1970/01/01から起算した秒数.
            refresh_token (str型): リフレッシュトークン.
    '''

    def __init__(self, access_token, access_token_expire_at, refresh_token):
        self.access_token = access_token
        self.access_token_expire_at = access_token_expire_at
        self.refresh_token = refresh_token
