from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings
from .routers import auth, products, cart, orders

class Settings(BaseSettings):
    CORS_ORIGINS: str = "http://localhost:3000"
    class Config:
        env_file = ".env", ".env.example"

settings = Settings()

app = FastAPI(title="Shop Backend (FastAPI)")

# CORS
origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(orders.router)

@app.get("/healthz")
def healthz():
    return {"status": "ok"}
