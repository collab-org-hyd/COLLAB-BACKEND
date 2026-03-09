# Backend

FastAPI backend application.

## Requirements

- [uv](https://docs.astral.sh/uv/) for Python package and environment management.
- Python 3.10+

## Setup

Install dependencies:

```bash
uv sync
```

## Running

### Development server (with hot reload)

```bash
uv run fastapi dev app/main.py
```

The API will be available at http://localhost:8000.  
Interactive docs (Swagger UI): http://localhost:8000/docs  
ReDoc: http://localhost:8000/redoc

> **Note:** Requires a running PostgreSQL instance. Start one with:
> ```bash
> docker compose up db -d
> ```

### With Docker Compose

From the project root:

```bash
docker compose watch
```

## Database Migrations

Migrations are managed with [Alembic](https://alembic.sqlalchemy.org).

**Apply all pending migrations:**

```bash
cd backend
uv run alembic upgrade head
```

**Create a new migration after changing models:**

```bash
uv run alembic revision --autogenerate -m "describe your change"
```

## Running Tests

```bash
cd backend
uv run bash scripts/tests-start.sh
```

Or directly with coverage:

```bash
uv run coverage run -m pytest tests/
uv run coverage report
uv run coverage html  # generates htmlcov/index.html
```

## Linting & Formatting

```bash
uv run ruff check .
uv run ruff format .
```

## Project Structure

```
app/
├── main.py          # FastAPI app entry point
├── models.py        # SQLModel database models
├── crud.py          # Database CRUD operations
├── utils.py         # Utility functions (email, tokens, etc.)
├── api/
│   ├── deps.py      # Shared dependencies (auth, DB session)
│   └── routes/      # API route handlers
├── core/
│   ├── config.py    # Settings (loaded from .env)
│   ├── db.py        # Database engine / session setup
│   └── security.py  # Password hashing, JWT
└── alembic/         # Database migration scripts
```
