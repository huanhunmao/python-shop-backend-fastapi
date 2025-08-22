from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException
from .models import User, Product, CartItem, Order, OrderItem
from .auth import get_password_hash, verify_password, create_access_token

# ---- Auth ----
def register_user(db: Session, email: str, password: str) -> User:
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(email=email, hashed_password=get_password_hash(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def login_user(db: Session, email: str, password: str) -> str:
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    return create_access_token(subject=user.email)

# ---- Products ----
def list_products(db: Session, q: str | None = None, skip: int = 0, limit: int = 20):
    stmt = select(Product)
    if q:
        stmt = stmt.filter(Product.name.ilike(f"%{q}%"))
    items = db.execute(stmt.offset(skip).limit(limit)).scalars().all()
    return items

def create_product(db: Session, name: str, description: str, price: float, stock: int) -> Product:
    p = Product(name=name, description=description or "", price=price, stock=stock)
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

# ---- Cart ----
def get_cart(db: Session, user_id: int):
    return db.query(CartItem).filter(CartItem.user_id == user_id).all()

def add_to_cart(db: Session, user_id: int, product_id: int, quantity: int) -> CartItem:
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    item = db.query(Ccart := CartItem).filter(Ccart.user_id == user_id, Ccart.product_id == product_id).first()
    if item:
        item.quantity += quantity
    else:
        item = CartItem(user_id=user_id, product_id=product_id, quantity=quantity)
        db.add(item)
    db.commit()
    db.refresh(item)
    return item

def update_cart_item(db: Session, user_id: int, item_id: int, quantity: int) -> CartItem:
    item = db.get(CartItem, item_id)
    if not item or item.user_id != user_id:
        raise HTTPException(status_code=404, detail="Cart item not found")
    if quantity <= 0:
        db.delete(item)
        db.commit()
        raise HTTPException(status_code=200, detail="Deleted")
    item.quantity = quantity
    db.commit()
    db.refresh(item)
    return item

def remove_cart_item(db: Session, user_id: int, item_id: int):
    item = db.get(CartItem, item_id)
    if not item or item.user_id != user_id:
        raise HTTPException(status_code=404, detail="Cart item not found")
    db.delete(item)
    db.commit()

# ---- Orders ----
def checkout(db: Session, user_id: int) -> Order:
    cart_items = db.query(CartItem).filter(CartItem.user_id == user_id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    # 事务：扣库存 + 写订单 + 清空购物车
    order = Order(user_id=user_id, total_amount=0.0)
    db.add(order)
    total = 0.0
    for ci in cart_items:
        product = db.get(Product, ci.product_id)
        if not product or product.stock < ci.quantity:
            raise HTTPException(status_code=400, detail=f"Not enough stock for product {ci.product_id}")
        product.stock -= ci.quantity
        subtotal = ci.quantity * product.price
        total += subtotal
        db.add(OrderItem(order=order, product_id=product.id, quantity=ci.quantity, unit_price=product.price, subtotal=subtotal))

    order.total_amount = total
    # 清空购物车
    for ci in cart_items:
        db.delete(ci)

    db.commit()
    db.refresh(order)
    return order

def list_my_orders(db: Session, user_id: int):
    return db.query(Order).filter(Order.user_id == user_id).order_by(Order.id.desc()).all()
