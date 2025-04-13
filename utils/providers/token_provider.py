import secrets
from datetime import datetime, timedelta
from typing import Dict, Optional

import jwt
from config import Config

from utils.exceptions.exception import UnauthorizedLogin

ALGORITHM = "HS256"
MINUTES = 3600


def new_salt():
    return secrets.token_hex(16)


def jwt_encoder(claims: dict, exp: int = MINUTES) -> str:
    salt = new_salt()
    data = claims.copy()
    secret = Config().SECRET_KEY

    # Creating expiry time
    expires = datetime.utcnow() + timedelta(minutes=exp)
    data.update({"exp": expires, "salt": salt})

    # Encoding jwt to return
    encoded_jwt = jwt.encode(data, secret, algorithm=ALGORITHM)

    return encoded_jwt


def verify_jwt_token(token: str) -> Optional[Dict]:
    secret = Config().SECRET_KEY

    try:
        data = jwt.decode(token, secret, algorithms=[ALGORITHM])
        return data
    except jwt.DecodeError:
        raise UnauthorizedLogin("Invalid token")
    except jwt.ExpiredSignatureError:
        raise UnauthorizedLogin("Token expired")
