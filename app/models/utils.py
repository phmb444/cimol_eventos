import hashlib
import hmac
from dotenv import load_dotenv
import os
load_dotenv()
SECRET = os.getenv("SECRET")

def encrypt_password(password: str) -> str:
    return hmac.new(SECRET.encode(), password.encode(), hashlib.sha256).hexdigest()

def compare_encrypted_passwords(encrypted_password: str, password: str) -> bool:
    return hmac.compare_digest(encrypted_password, encrypt_password(password))
