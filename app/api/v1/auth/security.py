from datetime import datetime, timedelta, timezone
from jose import jwt
from app.config import settings
import bcrypt
import hmac
import hashlib


def hash_password(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')


def verify_password(password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(
            password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    except Exception:
        return False


def create_token(data: dict, minutes: int):
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=minutes)
    payload.update({"exp": expire})

    return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)


def verify_telegram_auth(data: dict, bot_token: str) -> bool:
    if "hash" not in data:
        return False

    check_hash = data.pop("hash")

    allowed_keys = ["id", "first_name", "last_name", "username", "photo_url", "auth_date"]
    data_to_check = {k: v for k, v in data.items() if k in allowed_keys and v is not None}

    data_check_string = "\n".join([f"{k}={v}" for k, v in sorted(data_to_check.items())])

    secret_key = hashlib.sha256(bot_token.encode()).digest()
    hash_result = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    return hash_result == check_hash
