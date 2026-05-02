# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
uv sync

# Run development server (with hot reload)
uv run uvicorn main:application --reload

# Run with Docker Compose (includes PostgreSQL with seed data)
docker compose up --build
```

There is no test suite or linter configured in `pyproject.toml`. The Swagger UI at `http://localhost:8000/docs` is the primary way to exercise the API.

## Architecture

FastAPI + SQLAlchemy 2 REST API over a PostgreSQL sales dataset. The stack follows a strict four-layer pattern:

```
routers/ → crud/ → models/ → database
              ↓
           schemas/   (Pydantic DTOs, used only in routers and crud)
```

**`app/crud/base.py`** defines `BaseCRUD[ModelT, CreateT, UpdateT]` — a generic class providing `get`, `get_or_404`, `list`, `create`, `update`, `delete`. Every entity's CRUD class inherits from it and only adds a `list_filtered` method with entity-specific query filters. The `list` method accepts an optional `filters: list[Any]` that are passed directly to SQLAlchemy's `.filter(*filters)`.

**`app/models/__init__.py`** imports all ORM models so that `Base.metadata` registers every table before `create_all()` runs at startup. Adding a new model requires adding it here.

**PATCH semantics**: `update` calls `obj_in.model_dump(exclude_unset=True)` — only fields explicitly provided in the request body are written. All `Update` schemas use `Optional` fields with no defaults.

**`sales_order` primary key**: `sales_order.id` is `INTEGER PRIMARY KEY` (not `SERIAL`), so callers must supply the `id` on creation. Seed data uses IDs 10001–10240.

**Startup**: `Base.metadata.create_all(bind=engine)` runs via the FastAPI `lifespan` hook. It is idempotent and will not modify existing tables.

## Environment

Copy `.env.example` to `.env`:

```
APP_NAME="Sales Dataset API"
DEBUG=false
DATABASE_URL=postgresql+psycopg2://user:pass@localhost:5432/salesdataset
```

`DEBUG=true` enables SQLAlchemy query echo logging.

## Database

Schema and seed data live in `docs/schema.sql` and `docs/seeds.sql`. These are the source of truth for the table structure. Docker Compose mounts `docs/` as init scripts for the PostgreSQL container.
