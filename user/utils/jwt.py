import base64
import uuid
from cv001.settings import SECRET_KEY
import datetime
import jwt
from rest_framework_simplejwt.tokens import RefreshToken
sec = SECRET_KEY.encode('ascii')
encoded_key = base64.b64encode(sec)


def get_tokens_for_user(user):

    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def email_jwt(userinstance):
    claims = {"UID": str(userinstance.UID), "exp": datetime.datetime.utcnow(
    ) + datetime.timedelta(minutes=20), "iat": datetime.datetime.utcnow(), 'jti': str(uuid.uuid1())}
    encoded = str(jwt.encode(claims, encoded_key, algorithm="HS256"))
    spi = encoded.split("'")
    return spi[1]


def email_decode(token):
    try:
        dt = jwt.decode(token, encoded_key, algorithm="HS256")
        return dt['UID']
    except Exception as e:
        print(e)
        return False


def verification_jwt(userinstance):
    claims = {"exp": datetime.datetime.utcnow(
    ) + datetime.timedelta(minutes=10), 'jti': str(uuid.uuid1())}
    encoded = str(jwt.encode(claims, userinstance.UID, algorithm="HS256"))
    spi = encoded.split("'")
    return spi[1]


def verification_jwt_decode(token, userinstance):
    try:
        tokeninstance = jwt.decode(token, userinstance.UID, algorithm="HS256")
        return True
    except Exception as e:
        print(e)
        return False
