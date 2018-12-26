import datetime
import json
from jose import jwt, jws
import logging
from app.utils.config import config

log = logging.getLogger(__name__)


BEARER_PREFIX = "Bearer "

cognito_region = config.get("cognitoRegion")
cognito_userpool_id = config.get("cognitoUserPoolId")
userpool_keys_file = config.get("cognitoUserPoolKeysFile")
userpool_keys = []
with open(userpool_keys_file) as f:
    userpool_keys = json.load(f).get("keys")


def authorize_request(request):
    try:
        token = _retrieve_header_token(request)

        username = _get_username_from_token(token)
        if username is None:
            raise Exception("Username not found in token")

        userpool_iss = _cognito_userpool_iss(cognito_region, cognito_userpool_id)

        return _validate_jwt(token, userpool_iss, userpool_keys)
    except InvalidToken as e:
        raise e
    except Exception as e:
        raise InvalidToken(e)


def _retrieve_header_token(request):
    """Retrieve token from the header of the given request
    """
    token = request.headers.get("Authorization", None)
    if not token:
        raise Exception("No token found in header")
    if token.startswith(BEARER_PREFIX):
        token = token[len(BEARER_PREFIX):]
    return token


def _cognito_userpool_iss(cognito_region, cognito_userpool_id):
    """
    Return the iss of the Cognito User Pool
    :param cognito_region: string with region for Cognito User Pool
    :param cognito_userpool_id: string with Cognito User Pool ID
    :return: string with iss of the Cognito User Pool
    """
    return "https://cognito-idp.{}.amazonaws.com/{}".format(cognito_region, cognito_userpool_id)


def _validate_jwt(token, userpool_iss, userpool_keys):
    """
    Perform the token validation steps as per
    https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-using-tokens-with-identity-providers.html
    :param token: jwt string
    :param userpool_iss: string with url base to check issuer
    :param userpool_keys: json with JSON Web Keys of the User Pool
    :return: True if validation succeeds; False otherwise
    """
    log.debug("Validating token")

    # 2 Decode the token string into JWT format.
    jwt_headers = jwt.get_unverified_header(token)
    kid = jwt_headers["kid"]
    use_keys = [key for key in userpool_keys if key["kid"] == kid]
    if len(use_keys) != 1:
        raise InvalidToken("Obtained keys are wrong")
    use_key = use_keys[0]
    try:
        jwt.decode(token, use_key)
    except Exception as e:
        raise InvalidToken("Failed to decode token: {}".format(e))

    # 3 Check iss claim
    claims = jwt.get_unverified_claims(token)
    if claims["iss"] != userpool_iss:
        raise InvalidToken("Invalid issuer in token")

    # 4 Check token use
    # Should we only allow one of the tokens or both "id" and "access"?
    if claims["token_use"] not in ["id", "access"]:
        raise InvalidToken("Token not of valid use")

    # 5 Check kid
    jwk_kids = [obj["kid"] for obj in userpool_keys]
    if kid not in jwk_kids:
        # Should be here; condition 2 should have guaranteed this
        raise InvalidToken("Token is not related to id provider")

    # 6 Verify signature of decoded JWT?
    try:
        jws.verify(token, use_key, jwt_headers["alg"])
    except Exception as e:
        raise InvalidToken("Failed to verify signature {}".format(e))

    # 7 Check exp and make sure it is not expired
    exp = claims["exp"]
    exp_date = datetime.datetime.utcfromtimestamp(exp)
    now = datetime.datetime.utcnow()
    if exp_date < now:
        raise InvalidToken("Token has expired {}".format(exp_date - now))

    return claims


def _get_username_from_token(token):
    """
    Get unverified token expected cognito username from claims
    :param token: string with cognito JWT
    :return: string with username; None if unable to identify the username
    """
    claims = jwt.get_unverified_claims(token)
    # Example of claims of Access token =
    # {'scope': 'aws.cognito.signin.user.admin', 'exp': 1507256126,
    # 'sub': 'f1c4cf9f-8dea-446d-9900-xxxxxxxxxxxx',
    # 'client_id': 'xxxxxxxxxxxxxxxxxxxxxxxxxx',
    # 'token_use': 'access', 'iss': 'https://cognito-idp.ap-southeast-2.amazonaws.com/ap-southeast-2_xxxxxxxxx',
    # 'jti': 'd3c92f1c-61e5-4a02-85d8-509550667402', 'iat': 1507252526, 'username': 'user@example.com'}

    # Example of claims of Id token =
    # {'email': 'user@example.com', 'email_verified': True, 'exp': 1507256126,
    # 'sub': 'f1c4cf9f-8dea-446d-9900-xxxxxxxxxxxx',
    # 'token_use': 'id', 'iss': 'https://cognito-idp.ap-southeast-2.amazonaws.com/ap-southeast-2_xxxxxxxxx',
    # 'auth_time': 1507252526, 'aud': 'xxxxxxxxxxxxxxxxxxxxxxxxxx',
    # 'iat': 1507252526, 'cognito:username': 'user@example.com'}

    use = claims["token_use"]
    if use == "id":
        return claims["cognito:username"]
    if use == "access":
        return claims["username"]
    return None


class InvalidToken(BaseException):
    def __init__(self, message):
        self.message = "Token validation failed: {}".format(message)
