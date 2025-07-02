from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.balance import get_balance

router = APIRouter()

@router.get("/balance")
def balance(uid: str, db: Session = Depends(get_db)):
    bal = get_balance(uid, db)
    if bal is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"balance": bal}
