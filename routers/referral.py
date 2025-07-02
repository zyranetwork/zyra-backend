# routers/referral.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from models.user import User

router = APIRouter()

@router.post("/set-referral")
def set_referral(
    uid: str = Query(...),
    referral_code: str = Query(...),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter_by(google_uid=uid).first()
    if not user:
        raise HTTPException(404, "User not found")
    if user.has_claimed_referral:
        raise HTTPException(400, "Referral already claimed")
    if user.referral_code == referral_code:
        raise HTTPException(400, "Cannot refer yourself")

    inviter = db.query(User).filter_by(referral_code=referral_code).first()
    if not inviter:
        raise HTTPException(404, "Referral code invalid")

    user.power += 5
    inviter.power += 5
    user.referred_by = inviter.wallet_address
    user.has_claimed_referral = True
    db.commit()
    return {"message": "Referral applied", "inviter_uid": inviter.google_uid}

@router.get("/referrals")
def get_referrals(uid: str = Query(...), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(google_uid=uid).first()
    if not user:
        raise HTTPException(404, "User not found")
    referred = db.query(User).filter_by(referred_by=user.wallet_address).all()
    return {
        "total": len(referred),
        "referrals": [
            {"google_uid": u.google_uid, "email": u.email, "wallet": u.wallet_address}
            for u in referred
        ],
    }
