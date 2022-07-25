from v1_terminal.data.ICardActivateRepository import ICardActivateRepository
from v1_terminal.data.ITransactionGrantRepository import ITransactionGrantRepository
from v1_terminal.data.ITerminalAccessTokenRepository import ITerminalAccessTokenRepository
from v1_terminal.buisiness_logic.access_token.evaluate_access_token \
    import EvaluateAccessToken
from v1_terminal.buisiness_logic.access_token.common \
    import decode_token_to_json

from rest_framework import status

class TransactionGrant:
    '''
        TransactionGrantクラス

        Attributes:
            card_activate_repository(ICardActivateRepository型):
            ICardActivateRepositoryを継承したオブジェクト
            access_token_repository(ITerminalAccessTokenRepository型):
            ITerminalAccessTokenRepositoryを継承したオブジェクト
            transaction_grant_repository(ITransactionGrantRepository型):
            ITransactionGrantRepositoryを継承したオブジェクト
    '''

    def __init__(
        self, card_activate_repository: ICardActivateRepository,
        access_token_repository: ITerminalAccessTokenRepository,
        transaction_grant_repository: ITransactionGrantRepository,
    ):
        self.card_activate_repository: ICardActivateRepository =\
            card_activate_repository

        self.access_token_repository: ITerminalAccessTokenRepository =\
            access_token_repository

        self.transaction_grant_repository: ITransactionGrantRepository =\
            transaction_grant_repository


    def execute(
        self, pk, card_number, pin_number, access_token, amount, grant_method,
        grant_account, usage_restriction):

        evalueate_access_token = EvaluateAccessToken(self.access_token_repository)
        principal_id = evalueate_access_token.execute(access_token)

        if not principal_id:
            return None, status.HTTP_200_OK
        try:
            card = self.card_activate_repository.\
                identify_card(card_number, pin_number)
        except Exception as e:
            # 存在しないカード
            return None, status.HTTP_200_OK

        # service_user_policy=False, サービス利用許可なし
        if not card.service_user_policy:
            return None, status.HTTP_400_BAD_REQUEST

        # アクティベートでないカード
        if card.state != 1:
            return None, status.HTTP_400_BAD_REQUEST


        # provider_id='', 事業者が結びついていないカード
        if card.provider_id == '':
            return None, status.HTTP_400_BAD_REQUEST

        access_token_payload_json = decode_token_to_json(access_token)
        terminal_no = access_token_payload_json['terminal_no']

        grant = self.transaction_grant_repository.grant(pk,
                                                    card.card_no,
                                                    terminal_no,
                                                    amount,
                                                    grant_method,
                                                    grant_account,
                                                    usage_restriction)

        if not grant:
            return None, status.HTTP_400_BAD_REQUEST

        else:
            return grant, status.HTTP_200_OK