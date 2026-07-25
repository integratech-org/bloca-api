# Bloca Backend API (`bloca-api`)

Part of the **BLOCA** ecosystem — an IoT-monitored plastic-to-brick compactor with machine learning-based grading.

`bloca-api` is the core backend service powering compactor data collection, telemetry ingestion, user authentication, and coordination with machine learning grading pipelines.

## Features

- **Telemetry Ingestion:** High-throughput endpoints for IoT compactor sensor data (pressure, load, temperature, cycle stats).
- **Compactor & Device Management:** CRUD operations and state management for connected compaction hardware.
- **Authentication & Authorization:** Secure headless authentication powered by `django-allauth` and Django Ninja.
- **API Framework:** High-performance typed REST APIs using Django Ninja.

## Tech Stack

- **Language:** Python >= 3.14
- **Framework:** Django 6 & Django Ninja
- **Database:** PostgreSQL (`psycopg`)
- **Server:** Uvicorn / Gunicorn
- **Tooling:** `uv` (dependency management), Ruff (linting), Mypy (type checking)

## Project Structure

```text
bloca-api/
├── apps/
│   └── example/      # Core domain models, controllers, and services
├── config/
│   ├── api.py        # Django Ninja API router setup
│   ├── settings.py   # Django project settings
│   ├── urls.py       # Root URL configuration
│   └── wsgi.py / asgi.py
├── manage.py
├── main.py           # Application entry point
└── pyproject.toml
```

## Related Repositories

- [`bloca-admin`](https://github.com/integratech-org/bloca-admin) - Admin dashboard web UI
- [`bloca-firmware`](https://github.com/integratech-org/bloca-firmware) - IoT firmware sources
- [`bloca-ml`](https://github.com/integratech-org/bloca-ml) - Machine learning grading service
