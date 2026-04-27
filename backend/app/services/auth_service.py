import hashlib
import hmac
import os
from datetime import datetime, timedelta

from jose import jwt

from app.repositories.user_repository import create_user, get_user_by_email

SECRET_KEY = "muslimconnect-secret-key-change-in-production"
ALGORITHM = "HS256"
TOKEN_EXPIRE_HOURS = 24

def hash_password(password: str) -> str:
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return salt.hex() + ':' + key.hex()

def verify_password(password: str, stored: str) -> bool:
    salt_hex, key_hex = stored.split(':')
    salt = bytes.fromhex(salt_hex)
    key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return hmac.compare_digest(key.hex(), key_hex)

def create_token(user_id: int, email: str) -> str:
    expire = datetime.utcnow() + timedelta(hours=TOKEN_EXPIRE_HOURS)
    return jwt.encode({"sub": str(user_id), "email": email, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)

def register_user(first_name: str, last_name: str, email: str, password: str, campus: str = None):
    existing = get_user_by_email(email)
    if existing:
        return None, "Email already registered"
    password_hash = hash_password(password)
    user_id = create_user(first_name, last_name, email, password_hash, campus)
    token = create_token(user_id, email)
    return {"token": token, "user_id": user_id, "email": email, "first_name": first_name, "last_name": last_name}, None

def login_user(email: str, password: str):
    user = get_user_by_email(email)
    if not user:
        return None, "Invalid email or password"
    if not verify_password(password, user["password_hash"]):
        return None, "Invalid email or password"
    token = create_token(user["id"], email)
    return {"token": token, "user_id": user["id"], "email": email, "first_name": user["first_name"], "last_name": user["last_name"]}, None