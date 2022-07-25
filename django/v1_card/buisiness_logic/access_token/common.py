from authlib.jose import jwt
from os import environ
from utils.datetime_utility import (now,
                                    to_utc_timestamp,
                                    get_datetime_hours_later_from,
                                    get_datetime_days_later_from)
import json


def create_access_token(card_no):
    '''アクセストークンを発行する.

    authlib.jose.jwtを使用して、現時刻をもとにアクセストークン、リフレッシュトークンを発行する.

    アクセストークンの有効期限は、現時刻より１時間.

    リフレッシュトークンの有効期限は、現時刻より14日間

    署名は、環境変数 SECRET_KEY を使用する.

    Args:
        トークンのpayloadに含めるものを指定する.
        card_no (str型): カード番号.

    Returns:
        str型: アクセストークン
        int型: アクセストークン有効期限
        str型: リフレッシュトークン
        int型: リフレッシュトークン有効期限

    '''

    current_datetime = now()
    access_token_exp = int(
        to_utc_timestamp(
            get_datetime_hours_later_from(current_datetime, hours=1)
        ))
    refresh_token_exp = int(
        to_utc_timestamp(
            get_datetime_days_later_from(current_datetime, days=14)
        ))

    access_token_payload = {"card_no": card_no}
    refresh_token_payload = {"card_no": card_no}

    secret = environ["SECRET_KEY"]

    access_token = jwt.encode(
        {'alg': 'HS256'},
        access_token_payload,
        secret).decode('utf-8')
    refresh_token = jwt.encode(
        {'alg': 'HS256'},
        refresh_token_payload,
        secret).decode('utf-8')

    return (access_token, access_token_exp,
            refresh_token, refresh_token_exp)


def decode_token_to_json(token):

    secret = environ["SECRET_KEY"]

    payload = jwt.decode(token, secret)

    # payloadはJWTClaim型。JSONに変換する。
    payload_json = json.loads(json.dumps(payload))

    return payload_json
