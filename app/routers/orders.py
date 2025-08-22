from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import services, schemas
from ..deps import get_current_user

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/checkout", response_model=schemas.OrderOut)
def checkout(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return services.checkout(db, user_id=user.id)

@router.get("/me", response_model=List[schemas.OrderOut])
def my_orders(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return services.list_my_orders(db, user_id=user.id)
