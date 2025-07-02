# models/user.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id                  = Column(Integer, primary_key=True, index=True)
    google_uid          = Column(String, unique=True, index=True)
    email               = Column(String, unique=True, index=True)
    wallet_address      = Column(String, unique=True, index=True)
    encrypted_private_key = Column(String)
    passkey             = Column(String)
    referral_code       = Column(String, unique=True, index=True)
    power               = Column(Integer, default=100)

    referred_by         = Column(String, ForeignKey("users.wallet_address"), nullable=True)
    has_claimed_referral = Column(Boolean, default=False)

    # reverse relationship – lihat semua user yang diajak
    referrals           = relationship(
        "User",
        primaryjoin="User.wallet_address==foreign(User.referred_by)",
        viewonly=True,
    )
