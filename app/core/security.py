from datetime import datetime

import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from passlib.context import CryptContext

from app.core.exceptions import Forbidden
from app.settings import get_settings


settings = get_settings()
pwd_context = CryptContext(schemes="bcrypt")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_token(data: dict, token_lifetime: int) -> str:
    data = data.copy()
    expire = datetime.now().timestamp() + token_lifetime
    data.update({"exp": expire})
    return jwt.encode(
        data, key=settings.JWT_SECRET_KEY, algorithm=settings.JWT_ENCODE_ALGORITHM
    )


def get_token_payload(token: str, token_type: str) -> dict:
    try:
        token_payload = jwt.decode(
            token, key=settings.JWT_SECRET_KEY, algorithms=settings.JWT_ENCODE_ALGORITHM
        )
        return token_payload
    except ExpiredSignatureError:
        raise Forbidden(message="Token expired. Please login again.")
    except InvalidTokenError:
        raise Forbidden(message=f"Invalid {token_type} token.")
