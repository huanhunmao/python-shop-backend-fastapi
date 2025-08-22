import asyncio
import os
import pytest
from httpx import AsyncClient
from app.main import app
from app.init_db import main as init_db_main

@pytest.fixture(scope="session", autouse=True)
def _init_db():
    # 每次测试使用全新数据库
    if os.path.exists("shop.db"):
        os.remove("shop.db")
    init_db_main()
    yield
    if os.path.exists("shop.db"):
        os.remove("shop.db")

@pytest.mark.asyncio
async def test_flow():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # 登录 admin
        resp = await ac.post("/auth/login", json={"email":"admin@example.com","password":"Admin123!"})
        assert resp.status_code == 200, resp.text
        token = resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 获取商品
        resp = await ac.get("/products")
        assert resp.status_code == 200
        products = resp.json()
        assert len(products) >= 1
        pid = products[0]["id"]

        # 添加购物车
        resp = await ac.post("/cart/items", json={"product_id": pid, "quantity": 2}, headers=headers)
        assert resp.status_code == 200

        # 结算
        resp = await ac.post("/orders/checkout", headers=headers)
        assert resp.status_code == 200
        order = resp.json()
        assert order["total_amount"] > 0
