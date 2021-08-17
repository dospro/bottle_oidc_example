from urllib.parse import urlencode

import bottle
import requests
import jwt

import config

PUBLIC_ROUTES = ["/login", "/callback"]


def login():
    params = {
        "scope": "openid",
        "response_type": "code",
        "client_id": config.client_id,
        "redirect_uri": "http://localhost:8000/callback",
    }
    url = f"{config.oidc_server_base_url}/auth?" + urlencode(params)

    return bottle.redirect(url)


def callback():
    code = bottle.request.GET['code']
    payload = {
        "code": code,
        "client_id": config.client_id,
        "client_secret": config.client_secret,
        "grant_type": "authorization_code",
        "redirect_uri": "http://localhost:8000/callback",
    }
    result = requests.post(
        f"{config.oidc_server_base_url}/token",
        data=payload
    )
    result.raise_for_status()
    jwt_token = result.json()["id_token"]
    jwks_client = jwt.PyJWKClient(f"{config.oidc_server_base_url}/certs")
    decoded_token = jwt.decode(
        jwt_token,
        jwks_client.get_signing_key_from_jwt(jwt_token).key,
        algorithms=["RS256"],
        audience=config.client_id
    )
    print(decoded_token)
    bottle.response.content_type = "application/json"
    bottle.response.set_cookie("username", decoded_token["preferred_username"])
    return bottle.redirect("/")


def logout():
    bottle.response.delete_cookie("username", path="/")
    return bottle.redirect("/")


class OIDCPlugin:
    name = "OIDC Plugin"
    api = 2

    def __init__(self):
        pass

    def setup(self, app: bottle.Bottle):
        app.route('/login', method='get', callback=login)
        app.route('/callback', method='get', callback=callback)
        app.route('/logout', method='get', callback=logout)

    def __call__(self, func):
        def wrapper(*args, **argv):
            cookie = bottle.request.cookies.get('username', None)
            bottle.request.user = cookie
            return func(*args, **argv)

        return wrapper
