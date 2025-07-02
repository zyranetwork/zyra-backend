from datetime import datetime
from sqlalchemy import Column, Integer, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class MiningSession(Base):
    __tablename__ = "mining_sessions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime)
    power = Column(Integer, default=100)
    is_boosted = Column(Boolean, default=False)
    last_saved_time = Column(DateTime, default=datetime.utcnow)
    accumulated_coin = Column(Float, default=0.0)

class BoostLog(Base):
    __tablename__ = "boost_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    session_id = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
