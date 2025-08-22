from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import services, schemas
from ..deps import get_current_user

router = APIRouter(prefix="/cart", tags=["cart"])

@router.get("", response_model=List[schemas.CartItemOut])
def my_cart(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return services.get_cart(db, user_id=user.id)

@router.post("/items", response_model=schemas.CartItemOut)
def add_item(payload: schemas.CartItemCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return services.add_to_cart(db, user_id=user.id, product_id=payload.product_id, quantity=payload.quantity)

@router.patch("/items/{item_id}", response_model=schemas.CartItemOut)
def update_item(item_id: int, payload: schemas.CartItemCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return services.update_cart_item(db, user_id=user.id, item_id=item_id, quantity=payload.quantity)

@router.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    services.remove_cart_item(db, user_id=user.id, item_id=item_id)
    return {"ok": True}
