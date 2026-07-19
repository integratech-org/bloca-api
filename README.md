# bloca-api

Backend API service for BLOCA, built with Django + Django Ninja Extra.

## Tech stack

- Python 3.14
- Django 6
- Django Ninja + Ninja Extra
- django-allauth (headless mode)
- PostgreSQL
- uv (dependency and environment management)

## Prerequisites

- Python 3.14
- [uv](https://docs.astral.sh/uv/)
- PostgreSQL (or Docker Compose)

## Environment variables

Create `.env` from `.env.example`:

```bash
cp .env.example .env
```

Required variables:

- `DEBUG`
- `SECRET_KEY`
- `DATABASE_URL`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`

## Local development (uv)

```bash
# install dependencies
uv sync

# run migrations
uv run python manage.py migrate

# start API server
uv run python manage.py runserver
```

The app will be available at `http://localhost:8000`.

## Docker Compose development

```bash
docker compose up --build
```

This starts:

- `django` on port `8000`
- `postgres` on port `5432`

## Project structure

```txt
apps/
  example/      # sample app/controller/service/model
config/
  settings.py   # Django settings and env wiring
  urls.py       # root URL config
  api.py        # Ninja API registration
manage.py       # Django management entrypoint
```

## API routes (current)

- `GET /api/example/hello`
- Django admin: `/admin/`
- allauth routes: `/accounts/` and `/_allauth/`

## Quality checks

```bash
uv run ruff check .
uv run ruff format .
uv run mypy .
```
