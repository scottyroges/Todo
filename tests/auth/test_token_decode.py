from datetime import datetime

import pytest

from app.config import config
from app.auth import token_decode
from app.auth.token_decode import NoTokenError, InvalidTokenError
from app.utils.attrdict import AttrDict


@pytest.fixture()
def userpool_keys(mocker):
    mock_userpool_keys = mocker.patch.object(token_decode, "userpool_keys", [{
        "kid": "1kid"
    }])
    return mock_userpool_keys


@pytest.fixture()
def claims_identity(mocker):
    mock_claims = mocker.patch("jose.jwt.get_unverified_claims")
    mock_claims.return_value = {
        "token_use": "id",
        "cognito:username": "tester",
        "iss": "https://cognito-idp.us-east-2.amazonaws.com/" + config.get("cognitoUserPoolId"),
        "exp": 1546545878
    }
    return mock_claims


@pytest.fixture()
def claims_access(mocker):
    mock_claims = mocker.patch("jose.jwt.get_unverified_claims")
    mock_claims.return_value = {
        "token_use": "access",
        "username": "tester",
        "iss": "https://cognito-idp.us-east-2.amazonaws.com/" + config.get("cognitoUserPoolId"),
        "exp": 1546545878
    }
    return mock_claims


@pytest.fixture()
def headers(mocker):
    mock_headers = mocker.patch("jose.jwt.get_unverified_header")
    mock_headers.return_value = {
        "kid": "1kid",
        "alg": "1alg"
    }
    return headers


@pytest.fixture()
def unexpired_token(mocker):
    mock_datetime = mocker.patch("app.auth.token_decode.datetime")
    mock_datetime.utcfromtimestamp.return_value = datetime(2019, 12, 27)
    mock_datetime.utcnow.return_value = datetime(2018, 8, 3)
    return mock_datetime


@pytest.fixture()
def expired_token(mocker):
    mock_datetime = mocker.patch("app.auth.token_decode.datetime")
    mock_datetime.utcfromtimestamp.return_value = datetime(2019, 12, 27)
    mock_datetime.utcnow.return_value = datetime(2020, 8, 3)
    return mock_datetime


def test_authorize_request_valid_identity_token(userpool_keys,
                                                headers,
                                                claims_identity,
                                                unexpired_token,
                                                mocker):
    mocker.patch("jose.jwt.decode")
    mocker.patch("jose.jws.verify")

    request = AttrDict({
        "headers": {
            "Authorization": "mytoken"
        }
    })
    token_decode.authorize_request(request)
    claims_identity.assert_called_with("mytoken")


def test_authorize_request_valid_access_token(userpool_keys,
                                              headers,
                                              claims_access,
                                              unexpired_token,
                                              mocker):
    mocker.patch("jose.jwt.decode")
    mocker.patch("jose.jws.verify")

    request = AttrDict({
        "headers": {
            "Authorization": "mytoken"
        }
    })
    token_decode.authorize_request(request)
    claims_access.assert_called_with("mytoken")


def test_authorize_request_bearer_token(userpool_keys,
                                        headers,
                                        claims_identity,
                                        unexpired_token,
                                        mocker):
    mocker.patch("jose.jwt.decode")
    mocker.patch("jose.jws.verify")

    request = AttrDict({
        "headers": {
            "Authorization": "Bearer mytoken"
        }
    })
    token_decode.authorize_request(request)
    claims_identity.assert_called_with("mytoken")


def test_authorize_request_no_token():
    request = AttrDict({
        "headers": {}
    })
    with pytest.raises(NoTokenError):
        token_decode.authorize_request(request)


def test_authorize_request_no_username(headers,
                                       mocker):
    mock_claims = mocker.patch("jose.jwt.get_unverified_claims")
    mock_claims.return_value = {
        "cognito:username": "tester",
        "iss": "https://cognito-idp.us-east-2.amazonaws.com/us-east-2_GgKNcQC1D",
        "exp": 1546545878
    }

    request = AttrDict({
        "headers": {
            "Authorization": "mytoken"
        }
    })
    with pytest.raises(InvalidTokenError):
        token_decode.authorize_request(request)


def test_authorize_request_invalid_userpool_keys(headers,
                                                 claims_identity,
                                                 unexpired_token,
                                                 mocker):
    mocker.patch.object(token_decode, "userpool_keys", [{
        "kid": "invalid"
    }])

    request = AttrDict({
        "headers": {
            "Authorization": "mytoken"
        }
    })
    with pytest.raises(InvalidTokenError):
        token_decode.authorize_request(request)


def test_authorize_request_no_kid_in_userpool_keys(headers,
                                                   claims_identity,
                                                   unexpired_token,
                                                   mocker):
    mocker.patch.object(token_decode, "userpool_keys", [{}])

    request = AttrDict({
        "headers": {
            "Authorization": "mytoken"
        }
    })
    with pytest.raises(InvalidTokenError):
        token_decode.authorize_request(request)


def test_authorize_request_decode_error(userpool_keys,
                                        headers,
                                        claims_identity,
                                        unexpired_token,
                                        mocker):
    mock_decode = mocker.patch("jose.jwt.decode")
    mock_decode.side_effect = Exception

    request = AttrDict({
        "headers": {
            "Authorization": "mytoken"
        }
    })
    with pytest.raises(InvalidTokenError):
        token_decode.authorize_request(request)


def test_authorize_request_iss_claim_mismatch(userpool_keys,
                                              headers,
                                              unexpired_token,
                                              mocker):
    mocker.patch("jose.jwt.decode")

    mock_claims = mocker.patch("jose.jwt.get_unverified_claims")
    mock_claims.return_value = {
        "token_use": "id",
        "cognito:username": "tester",
        "iss": "https://cognito-idp.us-east-2.amazonaws.com/invalid",
        "exp": 1546545878
    }

    request = AttrDict({
        "headers": {
            "Authorization": "mytoken"
        }
    })
    with pytest.raises(InvalidTokenError):
        token_decode.authorize_request(request)


def test_authorize_request_iss_claim_mismatch(userpool_keys,
                                              headers,
                                              unexpired_token,
                                              mocker):
    mocker.patch("jose.jwt.decode")

    mock_claims = mocker.patch("jose.jwt.get_unverified_claims")
    mock_claims.return_value = {
        "token_use": "asdf",
        "cognito:username": "tester",
        "iss": "https://cognito-idp.us-east-2.amazonaws.com/invalid",
        "exp": 1546545878
    }

    request = AttrDict({
        "headers": {
            "Authorization": "mytoken"
        }
    })
    with pytest.raises(InvalidTokenError):
        token_decode.authorize_request(request)


def test_authorize_request_decode_error(userpool_keys,
                                        headers,
                                        claims_identity,
                                        unexpired_token,
                                        mocker):
    mocker.patch("jose.jwt.decode")
    mock_verify = mocker.patch("jose.jws.verify")
    mock_verify.side_effect = Exception

    request = AttrDict({
        "headers": {
            "Authorization": "mytoken"
        }
    })
    with pytest.raises(InvalidTokenError):
        token_decode.authorize_request(request)


def test_authorize_request_expired_token(userpool_keys,
                                         headers,
                                         claims_identity,
                                         expired_token,
                                         mocker):
    mocker.patch("jose.jwt.decode")
    mocker.patch("jose.jws.verify")

    request = AttrDict({
        "headers": {
            "Authorization": "mytoken"
        }
    })
    with pytest.raises(InvalidTokenError):
        token_decode.authorize_request(request)
