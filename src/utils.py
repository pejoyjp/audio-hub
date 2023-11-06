from passlib.context import CryptContext
from pydantic_settings import BaseSettings
from decouple import config
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(plain_password: str):
    return pwd_context.hash(plain_password)

class Settings(BaseSettings):
    access_token_expire_minutes: int = 30  # 30 minutes
    refresh_token_expire_minutes: int = 60 * 24 * 7  # 7 days
    algorithm: str = "HS256"
    jwt_secret_key: str = config('JWT_SECRET_KEY', default='your_default_secret_key')
    jwt_refresh_secret_key: str = config('JWT_REFRESH_SECRET_KEY', default='your_default_refresh_secret_key')

    class Config:
        env_file = ".env"

settings = Settings()

def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, settings.algorithm)
    return encoded_jwt

def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=settings.refresh_token_expire_minutes)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.jwt_refresh_secret_key, settings.algorithm)
    return encoded_jwt


