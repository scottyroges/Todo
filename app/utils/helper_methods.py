import base64
import hashlib
import hmac
import os


def to_camel_case(name):
    first, *rest = name.split('_')
    return first + ''.join(word.capitalize() for word in rest)


def get_hmac_digest(username):
    message = username + os.environ.get("cognitoClientId")
    dig = hmac.new(os.environ.get("cognitoClientSecretKey").encode(),
                   msg=message.encode('UTF-8'),
                   digestmod=hashlib.sha256).digest()
    return base64.b64encode(dig).decode()