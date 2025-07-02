from datetime import datetime
from sqlalchemy.orm import Session
from models.user import User
from models.mining import MiningSession

COIN_PER_POWER_PER_HOUR = 0.005  # 1 power = 0.005 coin/12h

def calc_reward(power: int, hours: float) -> float:
    return power * COIN_PER_POWER_PER_HOUR * hours

def get_balance(uid: str, db: Session):
    user = db.query(User).filter_by(google_uid=uid).first()
    if not user:
        return None

    now = datetime.utcnow()
    total = 0.0
    sessions = db.query(MiningSession).filter_by(user_id=user.id).all()

    for s in sessions:
        last = s.last_saved_time or s.start_time
        end = min(now, s.end_time)
        hours = max((end - last).total_seconds() / 3600, 0)
        est = calc_reward(s.power, hours)
        total += s.accumulated_coin + est

        # Simpan tiap ≥ 1 jam
        if hours >= 1:
            s.accumulated_coin += est
            s.last_saved_time = end
    db.commit()
    return round(total, 6)
