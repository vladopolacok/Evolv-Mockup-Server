#!/usr/bin/env python3
'''
Application: Vibrant Evolv Fake testing server
Description: Test server supports: own responses
     Author: Vlado Polacok
'''

import connexion
import mockedData
import json

from connexion.resolver import RestyResolver
from six.moves.urllib.request import urlopen
from flask import Flask, request, jsonify, _request_ctx_stack
from jose import jwt
from connexion.exceptions import OAuthProblem

# Settings
AUTH0_DOMAIN = 'dev-mqauy-jb.auth0.com'
API_AUDIENCE = 'http://mysite.com'
ALGORITHMS = ["RS256"]
SERVER_PORT = 8081
API_DEFINITION_FILE = 'dist-api.yml'

APP = connexion.FlaskApp(__name__)

# Token validation method


def token_info(access_token) -> dict:

    token = access_token
    jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer="https://"+AUTH0_DOMAIN+"/"
            )
        except jwt.ExpiredSignatureError:
            raise OAuthProblem('Token is expired', 401)

        except jwt.JWTClaimsError:
            raise OAuthProblem(
                'Invalid claims. Please check the audience and issuer', 401)

        except Exception:
            raise OAuthProblem(
                'Invaid token - unable to parse authentication', 401)

        _request_ctx_stack.top.current_user = payload

    return {'uid': payload['sub'], 'scope': payload['scope']}


# Run Flask server and load definition of API
if __name__ == '__main__':
    APP.add_api(API_DEFINITION_FILE)  # , resolver=RestyResolver('api'))
    APP.run(SERVER_PORT)
