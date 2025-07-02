from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models.user import User
from wallet_utils import decrypt_private_key

router = APIRouter()

class ExportRequest(BaseModel):
    google_uid: str
    passkey: str

@router.post("/export-private-key")
def export_private_key(data: ExportRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(google_uid=data.google_uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        private_key = decrypt_private_key(user.encrypted_private_key, data.passkey)
    except Exception:
        raise HTTPException(status_code=400, detail="Corrupted data or wrong passkey")

    return {"private_key": private_key}
