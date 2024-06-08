from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])


def hash_password(plaintext: str):
    return pwd_context.hash(plaintext)


def verify_password(plaintext: str, hashed: str):
    return pwd_context.verify(plaintext, hashed)
