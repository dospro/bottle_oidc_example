import hmac
import base64
import hashlib
import json

import jwt

from config import client_secret, rsa_public_key, client_id


class JWTDecodeError(Exception):
    pass


def b64url_decode(msg: bytes):
    return base64.urlsafe_b64decode(msg.decode() + "=" * divmod(len(msg), 4)[1])


def decode_jwt_token(token: str):
    jwks_client = jwt.PyJWKClient("http://localhost:8080/auth/realms/dospro/protocol/openid-connect/certs")
    decoded_token = jwt.decode(token, jwks_client.get_signing_key_from_jwt(token).key, algorithms=["RS256"], audience=client_id)
    # print(token)
    # parts = token.encode().split(b".")
    # # Must have 3 parts
    # if len(parts) != 3:
    #     raise JWTDecodeError("This seems not to be a jwt")
    #
    # header, body, sign = parts
    # message = b".".join([header, body])
    # # First hash
    # verified_sign = hmac.new(rsa_public_key.encode(), message, hashlib.sha256).digest()
    # verified_sign = base64.urlsafe_b64encode(verified_sign).replace(b"=", b"")
    # print(f"{sign} == {verified_sign}")
    # if verified_sign != sign:
    #     # raise JWTDecodeError("Verification failed")
    #     print("Verification failed")
    #
    # decoded_header = b64url_decode(header)
    # decoded_payload = b64url_decode(body)

    return decoded_token

    # decoded_json = {
    #     "header": json.loads(decoded_header),
    #     "payload": json.loads(decoded_payload),
    # }
    # return decoded_json


def validate_token(token: str):
    parts = token.encode().split(b".")
    if len(parts) != 3:
        raise JWTDecodeError("This seems not to be a valid jwt")

    header, body, sign = parts

    # Check the signing algorithm
    # Get the public key
    # Base64url-encoded Header + "." + Base64url-encoded Payload)
    # Hash the result
    # Encrypt, generate signature
    # base64 encode the result again
    pass
