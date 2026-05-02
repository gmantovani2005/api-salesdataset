# Sales Dataset API

REST API built with **FastAPI** and **SQLAlchemy** over an Online Sales PostgreSQL dataset. Provides full CRUD with filtering for every table and auto-generated Swagger documentation.

---

## Requirements

- Python 3.14+
- [uv](https://github.com/astral-sh/uv) package manager
- PostgreSQL (already running with the schema applied)

---

## Quick Start

```bash
# 1. Install dependencies
uv sync

# 2. Configure environment
cp .env.example .env
# Edit .env with your actual DATABASE_URL

# 3. Run the development server
uv run uvicorn main:application --reload

# 4. Open Swagger UI
# http://localhost:8000/docs
```

---

## Environment Variables

Copy `.env.example` to `.env` and fill in the values:

| Variable | Description | Example |
|---|---|---|
| `APP_NAME` | Title shown in Swagger UI | `Sales Dataset API` |
| `DEBUG` | Enables SQL query logging | `false` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+psycopg2://user:pass@localhost:5432/salesdataset` |

---

## Running with Docker Compose

> The Compose file is provided as a reference model. The PostgreSQL service is already running externally.

```bash
docker compose up --build
```

This spins up:
- **db**: PostgreSQL 16 with schema and seed data loaded automatically from `docs/`
- **app**: The FastAPI application on port 8000

---

## Running on Kubernetes

> The Kubernetes manifest is a reference model for deployment configuration.

```bash
# Create the secret with your database URL
kubectl create secret generic api-salesdataset-secrets \
  --from-literal=DATABASE_URL="postgresql+psycopg2://user:pass@host:5432/salesdataset"

# Apply the manifests
kubectl apply -f kubernetes.yml
```

---

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/categories` | List categories (`?name=`) |
| POST | `/categories` | Create category |
| GET | `/categories/{id}` | Get category by ID |
| PATCH | `/categories/{id}` | Partial update |
| DELETE | `/categories/{id}` | Delete |
| GET | `/regions` | List regions (`?name=`) |
| POST | `/regions` | Create region |
| GET | `/regions/{id}` | Get region by ID |
| PATCH | `/regions/{id}` | Partial update |
| DELETE | `/regions/{id}` | Delete |
| GET | `/payment-methods` | List payment methods (`?name=`) |
| POST | `/payment-methods` | Create payment method |
| GET | `/payment-methods/{id}` | Get by ID |
| PATCH | `/payment-methods/{id}` | Partial update |
| DELETE | `/payment-methods/{id}` | Delete |
| GET | `/products` | List products (`?name=`, `?category_id=`, `?min_price=`, `?max_price=`) |
| POST | `/products` | Create product |
| GET | `/products/{id}` | Get product by ID |
| PATCH | `/products/{id}` | Partial update |
| DELETE | `/products/{id}` | Delete |
| GET | `/sales-orders` | List orders (`?product_id=`, `?region_id=`, `?payment_method_id=`, `?date_from=`, `?date_to=`, `?min_total=`, `?max_total=`) |
| POST | `/sales-orders` | Create order (caller supplies `id`) |
| GET | `/sales-orders/{id}` | Get order by ID |
| PATCH | `/sales-orders/{id}` | Partial update |
| DELETE | `/sales-orders/{id}` | Delete |

All list endpoints also accept `?skip=0&limit=100` for pagination.

---

## Project Structure

```
api-salesdataset/
├── main.py                     # FastAPI application, router wiring, lifespan hook
├── pyproject.toml              # Project metadata and dependencies (managed by uv)
├── .env.example                # Template for required environment variables
├── .env                        # Local secrets — git-ignored, not committed
├── Dockerfile                  # Multi-stage Python 3.14 image build
├── docker-compose.yml          # Reference: app + PostgreSQL services
├── kubernetes.yml              # Reference: Deployment and Service manifests
│
├── app/
│   ├── core/
│   │   ├── config.py           # Application settings loaded from environment via pydantic-settings
│   │   └── database.py         # SQLAlchemy engine, session factory, Base class, get_db dependency
│   │
│   ├── models/
│   │   ├── __init__.py         # Imports all models so Base.metadata registers every table
│   │   ├── category.py         # ORM model for the `category` table
│   │   ├── region.py           # ORM model for the `region` table
│   │   ├── payment_method.py   # ORM model for the `payment_method` table
│   │   ├── product.py          # ORM model for the `product` table (FK → category)
│   │   └── sales_order.py      # ORM model for the `sales_order` table (FK → product, region, payment_method)
│   │
│   ├── schemas/
│   │   ├── category.py         # Pydantic DTOs: CategoryBase / CategoryCreate / CategoryUpdate / CategoryRead
│   │   ├── region.py           # Pydantic DTOs: RegionBase / RegionCreate / RegionUpdate / RegionRead
│   │   ├── payment_method.py   # Pydantic DTOs for PaymentMethod
│   │   ├── product.py          # Pydantic DTOs for Product (includes unit_price as Decimal)
│   │   └── sales_order.py      # Pydantic DTOs for SalesOrder — Create schema requires caller-supplied `id`
│   │
│   ├── crud/
│   │   ├── base.py             # Generic BaseCRUD[Model, CreateSchema, UpdateSchema] with get / list / create / update / delete
│   │   ├── category.py         # CategoryCRUD — list_filtered supports `name` (case-insensitive partial match)
│   │   ├── region.py           # RegionCRUD — list_filtered supports `name`
│   │   ├── payment_method.py   # PaymentMethodCRUD — list_filtered supports `name`
│   │   ├── product.py          # ProductCRUD — list_filtered supports `name`, `category_id`, `min_price`, `max_price`
│   │   └── sales_order.py      # SalesOrderCRUD — list_filtered supports 7 filter params (IDs, date range, revenue range)
│   │
│   └── routers/
│       ├── category.py         # APIRouter for /categories — 5 endpoints (list, create, get, update, delete)
│       ├── region.py           # APIRouter for /regions
│       ├── payment_method.py   # APIRouter for /payment-methods
│       ├── product.py          # APIRouter for /products
│       └── sales_order.py      # APIRouter for /sales-orders
│
└── docs/
    ├── schema.sql              # PostgreSQL schema — source of truth for all tables
    ├── seeds.sql               # 240 sample orders and 232 products across 6 categories
    ├── check-seeds.sql         # Verification queries for the seed data
    ├── data-sales.md           # Dataset field descriptions
    ├── project-sales.md        # Original project requirements
    ├── prompt-scriar-estrutura.md  # Initial scaffolding prompt
    └── Online Sales Data.csv   # Source CSV for the dataset
```

---

## Design Notes

- **PATCH semantics**: update endpoints only write fields that are explicitly provided (`exclude_unset=True`). Send only the fields you want to change.
- **sales_order `id`**: the `sales_order` table uses `INTEGER PRIMARY KEY` (not `SERIAL`), so the caller must supply the `id` on creation. Existing data uses IDs in the 10001–10240 range.
- **Filtering**: all `ilike` filters use parameterised queries via SQLAlchemy — no SQL injection risk.
- **Startup**: `Base.metadata.create_all()` runs on startup. It is idempotent — it will not drop or modify tables that already exist.
