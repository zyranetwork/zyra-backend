# routers/mining.py
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.user import User
from models.mining import MiningSession
from services.mining import boost_power

router = APIRouter()


@router.post("/start-mining")
def start_mining(uid: str, db: Session = Depends(get_db)):
    """Mulai sesi mining 12 jam menggunakan power permanen (bonus referral
    sudah terhitung di kolom user.power)."""
    user = db.query(User).filter_by(google_uid=uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    now = datetime.utcnow()
    active = (
        db.query(MiningSession)
        .filter(MiningSession.user_id == user.id, MiningSession.end_time > now)
        .first()
    )
    if active:
        raise HTTPException(status_code=400, detail="Mining already active")

    session = MiningSession(
        user_id=user.id,
        start_time=now,
        end_time=now + timedelta(hours=12),
        power=user.power,  # ← gunakan power permanen (termasuk bonus referral)
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    return {
        "start_time": session.start_time,
        "end_time": session.end_time,
        "power": session.power,
    }


@router.post("/boost-power")
def boost(uid: str, db: Session = Depends(get_db)):
    """Aktifkan boost 30 % sekali per sesi."""
    session, err = boost_power(uid, db)
    if err:
        raise HTTPException(
            status_code=404 if "User" in err else 400,
            detail=err,
        )

    return {
        "message": "Boost activated",
        "new_power": session.power,
        "valid_until": session.end_time,
    }
