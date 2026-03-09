# FastAPI Backend

## Technology Stack and Features

- ? [**FastAPI**](https://fastapi.tiangolo.com) — Python web framework for building APIs.
  - ?? [SQLModel](https://sqlmodel.tiangolo.com) — ORM for SQL database interactions.
  - ?? [Pydantic](https://docs.pydantic.dev) — Data validation and settings management.
  - ?? [PostgreSQL](https://www.postgresql.org) — SQL database.
  - ?? [Alembic](https://alembic.sqlalchemy.org) — Database migrations.
- ?? [uv](https://docs.astral.sh/uv/) — Python package and environment management.
- ?? [Docker Compose](https://www.docker.com) — For development and production.
- ?? Secure password hashing (Argon2/bcrypt).
- ?? JWT authentication.
- ?? Email-based password recovery.
- ?? [Mailcatcher](https://mailcatcher.me) — Local email testing.
- ? Tests with [Pytest](https://pytest.org) and coverage reporting.
- ?? [Traefik](https://traefik.io) — Reverse proxy / load balancer.

### Interactive API Documentation

Available at `http://localhost:8000/docs` when running locally.

## Quick Start

### Prerequisites

- [Docker](https://www.docker.com/) — for running PostgreSQL and the full stack.
- [uv](https://docs.astral.sh/uv/) — for local development without Docker.

**Install uv:**

```powershell
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Option 1 — Docker Compose (recommended)

Starts the backend, database, Traefik proxy, and Mailcatcher together:

```bash
docker compose watch
```

| Service | URL |
|---|---|
| Backend API | http://localhost:8000 |
| Interactive Docs (Swagger) | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |
| Adminer (DB UI) | http://localhost:8080 |
| Mailcatcher | http://localhost:1080 |
| Traefik UI | http://localhost:8090 |

### Option 2 — Local with uv

1. Start only the database:
   ```bash
   docker compose up db -d
   ```
2. Install dependencies and run the dev server:
   ```bash
   cd backend
   uv sync
   uv run fastapi dev app/main.py
   ```

The API will be at http://localhost:8000.

## Configuration

All configuration lives in the `.env` file at the project root. Before going to production, change at minimum:

- `SECRET_KEY`
- `FIRST_SUPERUSER_PASSWORD`
- `POSTGRES_PASSWORD`

**Generate a secret key:**

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

| Variable | Description | Default |
|---|---|---|
| `SECRET_KEY` | JWT signing key | `changethis` |
| `FIRST_SUPERUSER` | Initial admin email | `admin@example.com` |
| `FIRST_SUPERUSER_PASSWORD` | Initial admin password | `changethis` |
| `POSTGRES_SERVER` | DB host | `localhost` |
| `POSTGRES_USER` | DB user | `postgres` |
| `POSTGRES_PASSWORD` | DB password | `changethis` |
| `POSTGRES_DB` | DB name | `app` |
| `BACKEND_CORS_ORIGINS` | Allowed CORS origins (comma-separated) | `http://localhost` |
| `FRONTEND_HOST` | Base URL used in email links (e.g. password reset) | `http://localhost:5173` |
| `SMTP_HOST` | SMTP server for sending emails | _(empty)_ |
| `SENTRY_DSN` | Sentry error tracking DSN | _(empty)_ |

## Backend Development

See [backend/README.md](./backend/README.md) for backend-specific development docs (running tests, linting, migrations, etc).

## Development

See [development.md](./development.md) for Docker Compose workflows, local domain setup, and env configuration.

## Deployment

See [deployment.md](./deployment.md) for production deployment instructions with Traefik and Docker Compose.

## License

MIT
