# Python Shop Backend (FastAPI)

一个**可直接运行**的电商购物后端示例：包含用户注册/登录（JWT）、商品列表、购物车、下单结算、订单记录等核心能力。代码采用**分层结构（Router/Service/DAO）**、**依赖注入**与**类型约束**，便于二次开发与扩展。

> 技术栈：FastAPI + SQLAlchemy + SQLite + JWT（python-jose）+ passlib[bcrypt] + PyTest + Docker

---

## 亮点

- **清晰分层**：`routers`（HTTP 层） / `services`（业务） / `models&schemas`（数据） / `deps`（依赖&安全）
- **安全认证**：OAuth2 + JWT，密码哈希（bcrypt），最小权限（演示 `is_admin`）
- **事务一致性**：结算下单使用事务保证库存与订单一致（示例）
- **可测试性**：内置 `pytest` 与 `httpx` 的端到端测试样例
- **工程化**：`Makefile`、`Dockerfile`、`docker-compose.yml`、`pre-commit`（可选）
- **文档即代码**：集成 OpenAPI，可访问 `http://localhost:8000/docs`
- **CORS 支持**：便于前端本地调试

---

## 快速开始

### 1) 本地运行（Python 3.10+）

```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
# 初始化数据库并灌入示例数据
python -m app.init_db
# 启动服务
uvicorn app.main:app --reload
```

访问：`http://localhost:8000/docs`

### 2) Docker 运行

```bash
docker build -t shop-backend .
docker run -p 8000:8000 --env-file .env.example shop-backend
```

或 `docker compose up -d`。

---

## API 摘要

- **Auth**
  - `POST /auth/register` 注册
  - `POST /auth/login` 登录（返回 `access_token`）
- **Products**
  - `GET /products` 列表/搜索/分页
  - `POST /products` 创建（需管理员）
- **Cart**
  - `GET /cart` 获取当前用户购物车
  - `POST /cart/items` 添加商品（`product_id`, `quantity`）
  - `PATCH /cart/items/{item_id}` 更新数量
  - `DELETE /cart/items/{item_id}` 移除
- **Orders**
  - `POST /orders/checkout` 结算下单（从购物车生成订单）
  - `GET /orders/me` 我的订单

首次启动后，可用 `.env.example` 中的 `ADMIN_EMAIL/ADMIN_PASSWORD` 登录管理员，或在 `/auth/register` 自行注册并手动把该用户的 `is_admin` 字段设为 `true`（示例种子已包含管理员账号）。

---

## 环境变量（.env.example）

```env
SECRET_KEY=dev-super-secret-change-me
ACCESS_TOKEN_EXPIRE_MINUTES=60
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=Admin123!
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

> 未提供 `.env` 时，将使用合理的默认值（仅用于开发环境）。

---

## 目录结构

```
.
├── app
│   ├── main.py            # 应用入口 & CORS & 路由注册
│   ├── database.py        # DB 会话管理
│   ├── models.py          # ORM 模型
│   ├── schemas.py         # Pydantic 模型
│   ├── auth.py            # 密码哈希 / JWT / 认证工具
│   ├── deps.py            # 依赖注入（获取 DB、当前用户、管理员校验）
│   ├── services.py        # 业务服务层（商品/购物车/订单）
│   ├── init_db.py         # 初始化 & 种子数据
│   └── routers
│       ├── auth.py        # 注册、登录
│       ├── products.py    # 商品
│       ├── cart.py        # 购物车
│       └── orders.py      # 订单
├── tests
│   └── test_api.py        # 端到端测试示例
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── .env.example
└── pyproject.toml
```

---

## 测试

```bash
pytest -q
```

---

## 可扩展方向

- 接入 **Redis** 做购物车缓存与库存秒杀扣减
- 引入 **Alembic** 进行在线 Schema 迁移
- 拆分服务：下单→消息队列→库存/支付/通知 事件驱动
- 支付集成：对接第三方支付回调，订单状态机
- 可观测性：Prometheus 指标、结构化日志、追踪

---

## License

MIT
