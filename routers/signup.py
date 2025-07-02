import requests
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from wallet_utils import create_wallet, encrypt_private_key, generate_passkey

router = APIRouter()

GOOGLE_TOKEN_INFO_URL = "https://oauth2.googleapis.com/tokeninfo"

@router.post("/signup")
def signup(
    id_token: str,
    referral_code: str | None = Query(None),
    db: Session = Depends(get_db)
):
    # ====== DEV OVERRIDE ==========================================
    # Untuk pengembangan lokal tanpa Google Sign‑In
    google_uid = id_token                      # pakai token mentah sbg UID
    email = f"{id_token}@test.local"           # email dummy
    # ==============================================================

    # 2. Cek apakah user sudah ada
    user = db.query(User).filter_by(google_uid=google_uid).first()
    if user:
        # User sudah terdaftar, langsung login
        return {
            "id": user.id,
            "google_uid": user.google_uid,
            "email": user.email,
            "wallet_address": user.wallet_address,
            "passkey": user.passkey,
            "referral_code": user.referral_code
        }

    # 3. Buat wallet baru & simpan user baru
    pk, address = create_wallet()
    passkey = generate_passkey()                    # 👉 BUAT SEKALI SAJA
    enc_pk  = encrypt_private_key(pk, passkey)

    # 4. Proses referral jika ada
    referred_by = None
    extra_power = 0
    has_claimed_referral = False

    if referral_code:
        inviter = db.query(User).filter_by(referral_code=referral_code).first()
        if inviter and inviter.wallet_address != address:
            # Valid inviter, tambahkan 5 power ke inviter
            inviter.power += 5
            referred_by = inviter.wallet_address
            extra_power = 5
            has_claimed_referral = True
        else:
            raise HTTPException(status_code=400, detail="Kode referral tidak valid atau self-referral")

    new_user = User(
        google_uid=google_uid,
        email=email,
        wallet_address=address,
        encrypted_private_key=enc_pk,
        passkey=passkey,
        referral_code=address[-6:],
        power=100 + extra_power,
        referred_by=referred_by,
        has_claimed_referral=has_claimed_referral
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "id": new_user.id,
        "google_uid": new_user.google_uid,
        "email": new_user.email,
        "wallet_address": new_user.wallet_address,
        "passkey": new_user.passkey,
        "referral_code": new_user.referral_code
    }
