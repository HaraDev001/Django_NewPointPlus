from v1_terminal.data.ICardActivateRepository import ICardActivateRepository
from v1_terminal.data.ITransactionUseRepository import ITransactionUseRepository
from v1_terminal.data.ITerminalAccessTokenRepository import ITerminalAccessTokenRepository
from v1_terminal.buisiness_logic.access_token.evaluate_access_token \
    import EvaluateAccessToken
from v1_terminal.buisiness_logic.access_token.common \
    import decode_token_to_json

from rest_framework import status

class TransactionUse:
    '''
        TransactionUseクラス

        Attributes:
            card_activate_repository(ICardActivateRepository型):
            ICardActivateRepositoryを継承したオブジェクト
            access_token_repository(ITerminalAccessTokenRepository型):
            ITerminalAccessTokenRepositoryを継承したオブジェクト
            transaction_use_repository(ITransactionUseRepository型):
            ITransactionUseRepositoryを継承したオブジェクト
    '''

    def __init__(
        self, card_activate_repository: ICardActivateRepository,
        access_token_repository: ITerminalAccessTokenRepository,
        transaction_use_repository: ITransactionUseRepository,
    ):

        self.card_activate_repository: ICardActivateRepository =\
            card_activate_repository

        self.access_token_repository: ITerminalAccessTokenRepository =\
            access_token_repository

        self.transaction_use_repository: ITransactionUseRepository =\
            transaction_use_repository


    def execute(
        self, pk, card_info_list, access_token):

        evalueate_access_token = EvaluateAccessToken(self.access_token_repository)
        principal_id = evalueate_access_token.execute(access_token)

        if not principal_id:
            return None, status.HTTP_200_OK

        response_status = None
        try:
            for card_info in card_info_list:
                target_card = self.card_activate_repository.\
                    identify_card(card_info['card_no'], card_info['card_pin'])

                # service_user_policy=False, サービス利用許可なし
                if not target_card.service_user_policy:
                    response_status = status.HTTP_400_BAD_REQUEST
                    break

                # アクティベートでないカード
                if target_card.state != 1:
                    response_status = status.HTTP_400_BAD_REQUEST
                    break

                # provider_id='', 事業者が結びついていないカード
                if target_card.provider_id == '':
                    response_status = status.HTTP_400_BAD_REQUEST
                    break
        except Exception as e:
            # 存在しないカード
            return None, status.HTTP_200_OK

        #ここまでエラーなし
        if not response_status:
            access_token_payload_json = decode_token_to_json(access_token)
            terminal_no = access_token_payload_json['terminal_no']

            use_bonus = self.transaction_use_repository.use(pk, card_info_list, terminal_no)

            if not use_bonus:
                return None, status.HTTP_400_BAD_REQUEST

            else:
                return use_bonus, status.HTTP_200_OK,
        else:
            return None, response_status