# services/crypto.py
from cryptography.fernet import Fernet
import hashlib
import base64

def get_fernet_key(passkey: str) -> bytes:
    key = hashlib.sha256(passkey.encode()).digest()
    return base64.urlsafe_b64encode(key)

def decrypt_private_key(encrypted_data: str, passkey: str) -> str:
    fernet_key = get_fernet_key(passkey)
    fernet = Fernet(fernet_key)
    return fernet.decrypt(encrypted_data.encode()).decode()
