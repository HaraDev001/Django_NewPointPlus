from typing import Tuple
from enum import IntEnum
from django.core.signing import Signer, TimestampSigner
from django.core.signing import BadSignature, SignatureExpired
from datetime import timedelta


class SignerUtilityStatus(IntEnum):
    ''' ステータス設定値 '''
    ''' デフォルト期限 '''
    DEFAULT_EXPIRATION_TIME_AT_SECOND = 60*60
    ''' 正常終了 '''
    UNSIGN_FINISH = 0
    ''' 有効期限切れ '''
    UNSIGN_EXPIRED = 1
    ''' トークン異常 '''
    UNSIGN_BAD_SIGNATURE = 2


def sign_timestamp(signed_body: str) -> str:
    '''
    暗号署名（作成時間が含まれる）を行う

    Parameters
    ----------
    signed_body : str
        暗号署名する文字列

    Returns
    ----------
    value : str
        暗号署名されたトークン
    '''
    signer = TimestampSigner()
    value = signer.sign_object(signed_body)
    return value


def unsign_expiration_check(token: str, time_seconds: int = SignerUtilityStatus.DEFAULT_EXPIRATION_TIME_AT_SECOND) -> Tuple[int, str]:
    '''
    経過時間の確認をし暗号署名されたトークンの復元を行う

    Parameters
    ----------
    token : str
        暗号署名されたトークン
    time_seconds : int
        有効時間（秒で指定）

    Returns
    ----------
    SignerUtilityStatus : int
        ステータス（UNSIGN_FINISH=0, UNSIGN_EXPIRED=1, UNSIGN_BAD_SIGNATURE=2）
    value : str
        複合化された文字列
    '''
    try:
        signer = TimestampSigner()
        value = signer.unsign_object(token, max_age=timedelta(seconds=time_seconds))
        return SignerUtilityStatus.UNSIGN_FINISH, value
    except SignatureExpired:
        # 期限切れ
        return SignerUtilityStatus.UNSIGN_EXPIRED, '有効期限切れ'
    except BadSignature:
        # トークンが正しくない
        return SignerUtilityStatus.UNSIGN_BAD_SIGNATURE, '不正なトークン'


def sign(signed_body: str) -> str:
    '''
    暗号署名を行う

    Parameters
    ----------
    signed_body : str
        暗号署名する文字列

    Returns
    ----------
    value : str
        暗号署名されたトークン
    '''
    signer = Signer()
    value = signer.sign_object(signed_body)
    return value


def unsign(token: str) -> Tuple[int, str]:
    '''
    暗号署名されたトークンの復元を行う

    Parameters
    ----------
    token : str
        暗号署名されたトークン

    Returns
    ----------
    SignerUtilityStatus : int
        ステータス（UNSIGN_FINISH=0, UNSIGN_BAD_SIGNATURE=2）
    value : str
        複合化された文字列
    '''
    try:
        signer = Signer()
        value = signer.unsign_object(token)
        return SignerUtilityStatus.UNSIGN_FINISH, value
    except BadSignature:
        # トークンが正しくない
        return SignerUtilityStatus.UNSIGN_BAD_SIGNATURE, '不正なトークン'
