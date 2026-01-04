from datetime import datetime, timedelta, timezone
from jose import jwt
from app.config import settings
import bcrypt


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
