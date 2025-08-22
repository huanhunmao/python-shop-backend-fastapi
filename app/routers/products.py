from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import services, schemas
from ..deps import require_admin

router = APIRouter(prefix="/products", tags=["products"])

@router.get("", response_model=List[schemas.ProductOut])
def list_products(q: str | None = None, skip: int = 0, limit: int = Query(20, le=100), db: Session = Depends(get_db)):
    return services.list_products(db, q=q, skip=skip, limit=limit)

@router.post("", response_model=schemas.ProductOut)
def create_product(payload: schemas.ProductCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    p = services.create_product(db, payload.name, payload.description or "", payload.price, payload.stock)
    return p
