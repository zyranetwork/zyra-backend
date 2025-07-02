#wallet_utils.py
import hashlib, base64
from cryptography.fernet import Fernet
from eth_account import Account
import secrets

# ── helper
def _fernet_from_passkey(passkey: str) -> Fernet:
    key32 = hashlib.sha256(passkey.encode()).digest()        # 32‑byte
    fkey  = base64.urlsafe_b64encode(key32)                  # Fernet key
    return Fernet(fkey)

# ── wallet generation
def create_wallet():
    acct = Account.create()
    return acct.key.hex(), acct.address

def generate_passkey() -> str:
    return secrets.token_hex(8)                              # 16 hex chars

# ── encryption helpers
def encrypt_private_key(private_key: str, passkey: str) -> str:
    return _fernet_from_passkey(passkey).encrypt(private_key.encode()).decode()

def decrypt_private_key(encrypted: str, passkey: str) -> str:
    return _fernet_from_passkey(passkey).decrypt(encrypted.encode()).decode()
