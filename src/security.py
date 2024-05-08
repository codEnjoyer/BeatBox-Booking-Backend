from passlib.context import CryptContext

from fastapi_login import LoginManager

from src.main import SECRET, TOKEN_URL

manager = LoginManager(SECRET, TOKEN_URL, use_cookie=False)
pwd_context = CryptContext(schemes=["bcrypt"])


def hash_password(plaintext: str):
    return pwd_context.hash(plaintext)


def verify_password(plaintext: str, hashed: str):
    return pwd_context.verify(plaintext, hashed)