from sqlalchemy.orm import Session
from .database import Base, engine, SessionLocal
from .models import User, Product
from .auth import get_password_hash
from pydantic_settings import BaseSettings

class SeedSettings(BaseSettings):
    ADMIN_EMAIL: str = "admin@example.com"
    ADMIN_PASSWORD: str = "Admin123!"
    class Config:
        env_file = ".env", ".env.example"

def seed(db: Session):
    # admin
    settings = SeedSettings()
    admin = db.query(User).filter(User.email == settings.ADMIN_EMAIL).first()
    if not admin:
        admin = User(
            email=settings.ADMIN_EMAIL,
            hashed_password=get_password_hash(settings.ADMIN_PASSWORD),
            is_admin=True
        )
        db.add(admin)

    # products
    if db.query(Product).count() == 0:
        demo = [
            {"name": "机械键盘", "description": "RGB 热插拔 87 键", "price": 399.0, "stock": 50},
            {"name": "电竞鼠标", "description": "轻量化电竞鼠标", "price": 199.0, "stock": 100},
            {"name": "27 寸 4K 显示器", "description": "IPS 99% sRGB", "price": 1699.0, "stock": 20},
        ]
        for p in demo:
            db.add(Product(**p))

    db.commit()

def main():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed(db)
    finally:
        db.close()

if __name__ == "__main__":
    main()
