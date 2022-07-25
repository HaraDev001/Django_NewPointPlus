from v1_terminal.data.ICardActivateRepository import ICardActivateRepository
from v1_terminal.data.ITransactionChargeRepository import ITransactionChargeRepository
from v1_terminal.data.ITerminalAccessTokenRepository import ITerminalAccessTokenRepository
from v1_terminal.buisiness_logic.access_token.evaluate_access_token \
    import EvaluateAccessToken

from rest_framework import status

class TransactionCharge:
    '''
        TransactionChargeクラス

        Attributes:
            card_activate_repository(ICardActivateRepository型):
            ICardActivateRepositoryを継承したオブジェクト
            access_token_repository(ITerminalAccessTokenRepository型):
            ITerminalAccessTokenRepositoryを継承したオブジェクト
            transaction_charge_repository(ITransactionChargeRepository型):
            ITransactionChargeRepositoryを継承したオブジェクト
    '''

    def __init__(
        self, card_activate_repository: ICardActivateRepository,
        access_token_repository: ITerminalAccessTokenRepository,
        transaction_charge_repository: ITransactionChargeRepository,
    ):
        self.card_activate_repository: ICardActivateRepository =\
            card_activate_repository

        self.access_token_repository: ITerminalAccessTokenRepository =\
            access_token_repository

        self.transaction_charge_repository: ITransactionChargeRepository =\
            transaction_charge_repository


    def execute(
        self, pk, card, access_token, charge_amount, campaign_flag):
        try:
            card = self.card_activate_repository.\
                identify_card(card['card_no'], card['card_pin'])
        except Exception as e:
            # 存在しないカード
            return None, status.HTTP_200_OK


        evalueate_access_token = EvaluateAccessToken(self.access_token_repository)
        principal_id = evalueate_access_token.execute(access_token)
        if not principal_id:
            return None, status.HTTP_200_OK

        # service_user_policy=False, サービス利用許可なし
        if not card.service_user_policy:
            return None, status.HTTP_400_BAD_REQUEST

        # アクティベートでないカード
        if card.state != 1:
            return None, status.HTTP_400_BAD_REQUEST

        charge = self.transaction_charge_repository.charge(pk,
                                                            card.card_no, principal_id,
                                                            charge_amount, campaign_flag)

        if not charge:
            return None, status.HTTP_400_BAD_REQUEST
        else:
            return charge, status.HTTP_200_OK
