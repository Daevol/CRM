from datetime import datetime, timedelta
from typing import Optional

import hashlib
import hmac
from jose import JWTError, jwt

from .config import get_settings

settings = get_settings()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hmac.compare_digest(get_password_hash(plain_password), hashed_password)


def get_password_hash(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    except JWTError:
        return None
