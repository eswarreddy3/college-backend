import bcrypt
import jwt
import secrets
from datetime import datetime, timezone
from flask import current_app


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))


def generate_access_token(user_id: int, role: str) -> str:
    from app.config import config
    import os
    cfg = config[os.getenv('FLASK_ENV', 'development')]
    payload = {
        'sub': str(user_id),
        'role': role,
        'iat': datetime.now(timezone.utc),
        'exp': datetime.now(timezone.utc) + cfg.JWT_ACCESS_TOKEN_EXPIRES,
    }
    return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')


def generate_refresh_token(user_id: int) -> tuple[str, datetime]:
    from app.config import config
    import os
    cfg = config[os.getenv('FLASK_ENV', 'development')]
    expires_at = datetime.now(timezone.utc) + cfg.JWT_REFRESH_TOKEN_EXPIRES
    payload = {
        'sub': str(user_id),
        'type': 'refresh',
        'jti': secrets.token_hex(16),
        'exp': expires_at,
    }
    token = jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')
    return token, expires_at


def decode_token(token: str) -> dict:
    return jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])


def generate_activation_token() -> str:
    return secrets.token_urlsafe(32)
