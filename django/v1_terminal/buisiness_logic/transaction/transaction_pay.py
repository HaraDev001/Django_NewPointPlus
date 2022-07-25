from v1_terminal.data.ICardActivateRepository import ICardActivateRepository
from v1_terminal.data.ITransactionPayRepository import ITransactionPayRepository
from v1_terminal.data.ITerminalAccessTokenRepository import ITerminalAccessTokenRepository
from v1_terminal.buisiness_logic.access_token.evaluate_access_token \
    import EvaluateAccessToken
from v1_terminal.buisiness_logic.access_token.common \
    import decode_token_to_json

from rest_framework import status

class TransactionPay:
    '''
        TransactionPayクラス

        Attributes:
            card_activate_repository(ICardActivateRepository型):
            ICardActivateRepositoryを継承したオブジェクト
            access_token_repository(ITerminalAccessTokenRepository型):
            ITerminalAccessTokenRepositoryを継承したオブジェクト
            transaction_pay_repository(ITransactionPayRepository型):
            ITransactionPayRepositoryを継承したオブジェクト
    '''

    def __init__(
        self, card_activate_repository: ICardActivateRepository,
        access_token_repository: ITerminalAccessTokenRepository,
        transaction_pay_repository: ITransactionPayRepository,
    ):
        self.card_activate_repository: ICardActivateRepository =\
            card_activate_repository

        self.access_token_repository: ITerminalAccessTokenRepository =\
            access_token_repository

        self.transaction_pay_repository: ITransactionPayRepository =\
            transaction_pay_repository


    def execute(
        self, pk, card_info_list, access_token, payment_amount, campaign_flag):

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

            payment = self.transaction_pay_repository.pay(pk,
                                                    card_info_list,
                                                    terminal_no,
                                                    payment_amount,
                                                    campaign_flag)

            if not payment:
                return None, status.HTTP_400_BAD_REQUEST

            else:
                return payment, status.HTTP_200_OK,
        else:
            return None, response_status