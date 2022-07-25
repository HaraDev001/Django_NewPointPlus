from rest_framework import status

from v1_terminal.data.ITransactionCancelRepository import ITransactionCancelRepository

from v1_terminal.buisiness_logic.access_token.common import decode_token_to_json

from utils.datetime_utility import (now,
                                    to_utc_timestamp
                                    )


class CancelTransaction:
    '''取引を取り消すクラス

        Attributes:
            repository (ITransactionCancelRepository型):
                    ITransactionCancelRepositoryを継承したオブジェクト
    '''

    def __init__(self, repository: ITransactionCancelRepository):
        self.repository: ITransactionCancelRepository = repository

    def execute(
               self,
               terminal_access_token,
               card_no,
               card_pin,
               magnetic_infomation,
               transaction_id,
               cancel_target_transaction_id):
        '''取引を取り消す.

        Args:
            terminal_access_token (str型): 店舗端末アクセストークン
            card_no (str型): カード番号.
            card_pin(str型): カードPIN番号
            magnetic_infomation (str型): 磁気情報
            transaction_id (str型): 取引番号. 取引番号発行APIによって発行された番号
            cancel_transaction_id (str型) : 取り消し対象の取引番号

        Returns:
            取引種別: 取り消した取引種別.
            取引日時: 取消の日時

        Raises:
            Exception: リクエストされたメールアドレス、パスワードで一致する店舗端末情報がない
            Exception: リクエストされた店舗端末番号で一致する店舗端末情報がない

        '''

        # 店舗端末アクセストークンからメールアドレス、店舗端末を取得する。
        token_payload_json = decode_token_to_json(terminal_access_token)

        mail_address = token_payload_json['mail_address']
        terminal_no = token_payload_json['terminal_no']

        terminal_access_token_repository = self.repository.terminal_access_token_repository
        try:
            # 店舗端末情報を取得する。
            terminal = terminal_access_token_repository.get_terminal(terminal_no)
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
            target_token_info = terminal_access_token_repository.get_terminal_access_authorization(
                mail_address, terminal_no
            )
        except Exception:
            # 店舗端末認証情報が取得できなかった。
            # 現状、200しか定義されていない
            return None, status.HTTP_200_OK

        # 店舗端末アクセストークンの有効チェック
        current_unixtime = int(to_utc_timestamp(now()))

        terminal_token_is_valid = \
            (target_token_info.state == 1) and (current_unixtime <= target_token_info.access_token_expire_at)

        if not terminal_token_is_valid:
            # 店舗端末アクセストークンは有効ではない
            # 現状、200しか定義されていない
            return None, status.HTTP_200_OK

        card_access_token_repository = self.repository.card_access_token_repository

        # カード情報を取得
        try:
            card = card_access_token_repository.identify_card(card_no, card_pin)
        except Exception:
            # カード番号に一致するカードがない
            # カード番号&PIN番号に一致するカードがない
            return None, status.HTTP_400_BAD_REQUEST

        if (card.service_user_policy is False):
            # サービス利用許可なし
            # 現状、200しか定義されていない
            return None, status.HTTP_200_OK

        # カードはアクティベートされているかチェック
        # state == 1 でアクティベート済みは、仮の状態。モデルが定義されたら書き換える。
        card_token_is_valid = (card.state == 1)
        if not card_token_is_valid:
            # カードアクセストークンは有効ではない
            # 現状、200しか定義されていない
            return None, status.HTTP_200_OK

        try:
            self.repository.get_transaction(cancel_target_transaction_id)
        except Exception:
            # 取り消したい取引がない
            return None, status.HTTP_200_OK

        try:
            transaction_cancel_response = self.repository.cancel_transaction(
                terminal, transaction_id, cancel_target_transaction_id)
        except Exception as e:
            return None, status.HTTP_200_OK

        return transaction_cancel_response, status.HTTP_200_OK
