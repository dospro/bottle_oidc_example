from urllib.parse import urlencode

import bottle
import requests
import jwt

from config import client_id, client_secret

PUBLIC_ROUTES = ["/login", "/callback"]


def login():
    params = {
        "scope": "openid",
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": "http://localhost:8000/callback",
    }
    url = "http://localhost:8080/auth/realms/dospro/protocol/openid-connect/auth?" + urlencode(params)

    return bottle.redirect(url)


def callback():
    code = bottle.request.GET['code']
    payload = {
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "authorization_code",
        "redirect_uri": "http://localhost:8000/callback",
    }
    result = requests.post(
        "http://localhost:8080/auth/realms/dospro/protocol/openid-connect/token",
        data=payload
    )
    result.raise_for_status()
    jwt_token = result.json()["id_token"]
    jwks_client = jwt.PyJWKClient("http://localhost:8080/auth/realms/dospro/protocol/openid-connect/certs")
    decoded_token = jwt.decode(
        jwt_token,
        jwks_client.get_signing_key_from_jwt(jwt_token).key,
        algorithms=["RS256"],
        audience=client_id
    )
    print(decoded_token)
    bottle.response.content_type = "application/json"
    bottle.response.set_cookie("username", decoded_token["preferred_username"])
    return bottle.redirect("/")


def logout():
    bottle.response.delete_cookie("username", path="/")
    return bottle.redirect("/")


class OIDCPlugin:
    def __init__(self):
        pass

    def setup(self, app: bottle.Bottle):
        app.route('/login', method='get', callback=login)
        app.route('/callback', method='get', callback=callback)
        app.route('/logout', method='get', callback=logout)

    def apply(self, func, route):
        cookie = bottle.request.get_cookie('username', None)
        is_authenticated = True if cookie else False
        if is_authenticated or bottle.request.path in PUBLIC_ROUTES:
            bottle.request.user = cookie
            return func
        else:
            return bottle.abort(401, "Sorry, access denied")
