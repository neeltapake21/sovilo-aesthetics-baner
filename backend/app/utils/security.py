import os
import hashlib
import secrets
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt, JWTError

pwd_context = CryptContext(
    schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=int(os.getenv("BCRYPT_ROUNDS", 12))
)

JWT_SECRET = os.getenv("JWT_SECRET") or os.getenv("JWT_SECRET_KEY") or ""
JWT_REFRESH_SECRET = os.getenv("JWT_REFRESH_SECRET") or os.getenv("JWT_REFRESH_SECRET_KEY") or ""
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()

def create_access_token(patient_id: str, email: str, expires_minutes: int = None) -> str:
    expire = datetime.utcnow() + timedelta(
        minutes=int(expires_minutes or os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    )
    payload = {"sub": patient_id, "email": email, "type": "access", "exp": expire}
    return jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)

def create_refresh_token(patient_id: str, remember_me: bool = True) -> str:
    days = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 30)) if remember_me else 1
    expire = datetime.utcnow() + timedelta(days=days)
    payload = {"sub": patient_id, "type": "refresh", "exp": expire, "jti": secrets.token_hex(16)}
    return jwt.encode(payload, JWT_REFRESH_SECRET, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict:
    payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
    if payload.get("type") != "access":
        raise JWTError("Not an access token")
    return payload

def decode_refresh_token(token: str) -> dict:
    payload = jwt.decode(token, JWT_REFRESH_SECRET, algorithms=[ALGORITHM])
    if payload.get("type") != "refresh":
        raise JWTError("Not a refresh token")
    return payload
