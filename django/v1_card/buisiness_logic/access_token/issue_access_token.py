from rest_framework import status

from v1_card.data.IAccessTokenRepository import IAccessTokenRepository
from v1_card.buisiness_logic.DTO.access_token_issue_response import AccessTokenIssueResponse

from .common import create_access_token


class IssueAccessToken:
    '''アクセストークンを発行するクラス

        アクセストークンを発行する

        Attributes:
            repository (IAccessTokenRepository型): IAccessTokenRepositoryを継承したオブジェクト
    '''

    def __init__(self, repository: IAccessTokenRepository):
        self.repository: IAccessTokenRepository = repository

    def execute(self, card_no, card_pin):
        '''アクセストークンを発行する.

        カード情報を取得後、
        1) PIN番号が一致するかを確認する.
        2) 決済可能なカードである、サービス利用許可あり、事業者利用規約に同意済み、を確認する.
        3) カードはアクティベートされていることを確認する.

        1), 2), 3) すべて満たされれば、アクセストークンを発行し、「有効」なカードアクセス認証情報として保存する.

        1), 2) まで満たされていれば、「未発行」のカードアクセス認証情報として保存する。アクセストークンを発行しない.

        それ以外はカードアクセス認証情報を保存しない。アクセストークンを発行しない.

        Args:
            card_no (str型): カード番号.
            card_pin (str型): カードPIN番号.

        Returns:
            AccessTokenIssueResponse型: アクセストークン, アクセストークン有効期限, リフレッシュトークンを含む.
            int型: HTTPステータスコード

        '''

        # カード情報を取得
        try:
            card = self.repository.identify_card(card_no, card_pin)
        except Exception:
            # カード番号に一致するカードがない
            # カード番号&PIN番号に一致するカードがない
            return None, status.HTTP_400_BAD_REQUEST

        if (card.payment is False or
                card.service_user_policy is False or
                card.company_user_policy is False):
            # 決済可能なカードではない、サービス利用許可なし、事業者利用規約に未同意
            return None, status.HTTP_403_FORBIDDEN

        # カードはアクティベートされているかチェック
        # state == 1 でアクティベート済みは、仮の状態。モデルが定義されたら書き換える。
        if card.state == 1:
            # カードはアクティベートされている
            token = create_access_token(card_no)

            # アクセストークンの状態：1 (有効)
            # 仮の状態。モデルが定義されたら書き換える。
            access_token_state = 1

            # カードアクセス認証情報を保存
            card_access_auth = \
                self.repository.get_or_create_card_access_authorization(card_no)

            card_access_auth.card_no = card_no
            card_access_auth.access_token = token[0]
            card_access_auth.access_token_expire_at = token[1]
            card_access_auth.refresh_token = token[2]
            card_access_auth.refresh_token_expire_at = token[3]
            card_access_auth.state = access_token_state

            self.repository.save_card_access_authorization(card_access_auth)

            return (
                AccessTokenIssueResponse(
                    access_token=token[0],
                    access_token_expire_at=token[1],
                    refresh_token=token[2]
                    ), status.HTTP_200_OK
                )

        else:
            # アクセストークンの状態：0 (未発行)
            # 仮の状態。モデルが定義されたら書き換える。
            access_token_state = 0

            # カードアクセス認証情報を保存
            card_access_auth = \
                self.repository.get_or_create_card_access_authorization(card_no)

            card_access_auth.card_no = card_no
            card_access_auth.access_token = None
            card_access_auth.access_token_expire_at = -1
            card_access_auth.refresh_token = None
            card_access_auth.refresh_token_expire_at = -1
            card_access_auth.state = access_token_state

            self.repository.save_card_access_authorization(card_access_auth)

            return None, status.HTTP_200_OK
