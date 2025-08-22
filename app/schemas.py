from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List

# ---- Auth ----
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserOut(BaseModel):
    id: int
    email: EmailStr
    is_admin: bool
    class Config:
        from_attributes = True

# ---- Product ----
class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = ""
    price: float
    stock: int = 0

class ProductOut(BaseModel):
    id: int
    name: str
    description: str
    price: float
    stock: int
    class Config:
        from_attributes = True

# ---- Cart ----
class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(ge=1)

class CartItemOut(BaseModel):
    id: int
    product: ProductOut
    quantity: int
    class Config:
        from_attributes = True

# ---- Orders ----
class OrderItemOut(BaseModel):
    product_id: int
    quantity: int
    unit_price: float
    subtotal: float
    class Config:
        from_attributes = True

class OrderOut(BaseModel):
    id: int
    total_amount: float
    items: List[OrderItemOut]
    class Config:
        from_attributes = True
