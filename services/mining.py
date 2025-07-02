from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models.mining import MiningSession, BoostLog
from models.user import User

def start_mining(uid: str, db: Session):
    user = db.query(User).filter_by(google_uid=uid).first()
    if not user:
        return None, "User not found"

    now = datetime.utcnow()
    active = db.query(MiningSession).filter(
        MiningSession.user_id == user.id,
        MiningSession.end_time > now
    ).first()
    if active:
        return active, None

    session = MiningSession(
        user_id=user.id,
        start_time=now,
        end_time=now + timedelta(hours=12),
        power=100
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session, None

def boost_power(uid: str, db: Session):
    user = db.query(User).filter_by(google_uid=uid).first()
    if not user:
        return None, "User not found"

    now = datetime.utcnow()
    session = db.query(MiningSession).filter(
        MiningSession.user_id == user.id,
        MiningSession.end_time > now
    ).first()
    if not session:
        return None, "No active mining session"

    if session.is_boosted or db.query(BoostLog).filter_by(session_id=session.id).first():
        return None, "Boost already used in this session"

    session.power = int(session.power * 1.3)
    session.is_boosted = True
    db.add(BoostLog(user_id=user.id, session_id=session.id))
    db.commit()
    return session, None
